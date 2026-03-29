import os
import sys
from google.adk.agents import LlmAgent
from google.adk.apps.app import App

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from adk_utils.plugins import Graceful429Plugin

graceful_plugin = Graceful429Plugin(
    name="graceful_429_plugin",
    fallback_text={
        "example.com": "**[Simulated Response via 429 Graceful Fallback]**\n\nContent from http://example.com:\n\nExample Domain\nThis domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.",
        "default": "**[Simulated Response via 429 Graceful Fallback]**\n\nThe web reading tool is currently out of quota. Please retry later."
    }
)
from google.adk.models import Gemini
from google.genai.types import HttpRetryOptions
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, \
                    StdioServerParameters, StdioConnectionParams

# IMPORTANT: Replace this with the ABSOLUTE path to your adk_server.py script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = "/home/YOUR_PROJECT_ID/adk_mcp_tools/adk_mcp_server/adk_server.py"

RETRY_OPTIONS = HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)

if PATH_TO_YOUR_MCP_SERVER_SCRIPT == "None":
    print("WARNING: PATH_TO_YOUR_MCP_SERVER_SCRIPT is not set. Please update it in agent.py.")
    # Optionally, raise an error if the path is critical

root_agent = LlmAgent(
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    name='web_reader_mcp_client_agent',
    instruction="""
        Use the 'load_web_page' tool to fetch content from a URL
        provided by the user.
     """,
    ## Add the MCPToolset below:
tools=[
    MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python3", # Command to run your MCP server script
            args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT], # Argument is the path to the script
        ),
        timeout=15,
        ),
        tool_filter=['load_web_page'] # Optional: ensure only specific tools are loaded
    )
],
)

graceful_plugin.apply_429_interceptor(root_agent)

app = App(
    name="adk_mcp_server",
    root_agent=root_agent,
    plugins=[graceful_plugin]
)
# UNCOMMENT THE LINE BELOW TO TEST FAILOVER:
# graceful_plugin.apply_test_failover(root_agent)
