# 🚀 Building-ADK-Agents-with-MCP-Integration

## 📌 Overview
This project implements **Model Context Protocol (MCP)** with **Google Agent Development Kit (ADK)** to:
* Use external MCP tools (Google Maps)
* Build a custom MCP server
* Enable tool-based AI agent workflows

This project is based on the official Google Skills lab **GENAI124**. 

# 🧠 What is MCP?
Model Context Protocol (MCP) is an open standard that enables LLMs to interact with external tools, APIs, and data sources using a client-server architecture. 

# 🎯 Objectives
* Use ADK agent as MCP client
* Integrate Google Maps MCP server
* Build custom MCP server
* Enable tool execution via agents

# 📂 Project Structure
```bash
adk_mcp_tools/
│
├── adk_mcp_server/
├── google_maps_mcp_agent/
├── callback_logging.py
├── requirements.txt

adk_utils/
├── plugins.py
```

# ⚙️ Setup & Installation (Task 1 - Lab)

## Step 1: Download Lab Files
```bash
gcloud storage cp -r gs://YOUR_GCP_PROJECT_ID-bucket/* .
```
## Step 2: Install ADK
```bash
export PATH=$PATH:"/home/${USER}/.local/bin"
python3 -m pip install google-adk -r adk_mcp_tools/requirements.txt
```

# 🔑 Task 2: Google Maps MCP Integration

## Step 1: Create API Key
* Go to **Google Cloud Console → Credentials**
* Click **Create API Key**
* Rename it to:
```
GOOGLE_MAPS_API_KEY
```
## Step 2: Create `.env` File
```bash
cd ~/adk_mcp_tools
cat << EOF > google_maps_mcp_agent/.env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=Project
GOOGLE_CLOUD_LOCATION=global
GOOGLE_MAPS_API_KEY="YOUR_API_KEY"
MODEL=gemini_flash_model_id
EOF
```
## Step 3: Copy `.env`
```bash
cp google_maps_mcp_agent/.env adk_mcp_server/.env
```
## Step 4: Add MCPToolset in `agent.py`
```python
tools=[
    MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": google_maps_api_key
                }
            ),
            timeout=15,
        ),
    )
]
```
## Step 5: Run ADK UI
```bash
cd ~/adk_mcp_tools
adk web --allow_origins "regex:https://.*\.cloudshell\.dev"
```
## Step 6: Open UI
```
http://127.0.0.1:8000
```
## Step 7: Test Prompts
```
Get directions from GooglePlex to SFO
```
```
What's the route from Paris, France to Berlin, Germany?
```

# 🧩 Task 3: Custom MCP Server

## Step 1: Update Path in agent.py
```python
PATH_TO_YOUR_MCP_SERVER_SCRIPT = "/home/USERNAME/adk_mcp_tools/adk_mcp_server/adk_server.py"
```
## Step 2: Add MCPToolset
```python
tools=[
    MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="python3",
                args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT],
            ),
            timeout=15,
        ),
        tool_filter=['load_web_page']
    )
]
```
## Step 3: Run MCP Server
```bash
python3 ~/adk_mcp_tools/adk_mcp_server/adk_server.py
```
## Step 4: Start ADK UI (New Terminal)
```bash
cd ~/adk_mcp_tools
adk web --allow_origins "regex:https://.*\.cloudshell\.dev"
```
## Step 5: Test Agent
```
Select: adk_mcp_server
```
```
Load the content from http://example.com
```

# 🌍 Running on Personal Google Cloud Account (Extra Setup)
## 🔧 What You Need To Set Up

### 1. Enable Billing 💰
* Go to **Billing → Enable billing**
* Required for API usage

### 2. Enable Required APIs
Go to **APIs & Services → Library** and enable:
* Vertex AI API
* Directions API
* Routes API
* (Optional) Maps JavaScript API

### 3. Create API Key
* Go to **Credentials → Create API Key**
* Restrict it to:

  * Maps APIs (Directions / Routes)

### 4. Set IAM Permissions
Ensure your account has:
* Owner / Editor role
* OR required service roles

### 5. Install ADK Locally
```bash
pip install google-adk
```

### 6. Update `.env`
```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_MAPS_API_KEY=your_api_key
MODEL=gemini-1.5-flash
```

### 7. Run Project
```bash
cd adk_mcp_tools
adk web
```

# 🔄 How It Works
### Flow:
1. ADK Agent → MCPToolset
2. MCPToolset → MCP Server
3. Tool execution (`load_web_page` / Maps)
4. Response → Agent

# ✨ Key Features
* Google Maps integration
* Custom MCP server
* Tool-based AI interaction
* Standardized MCP communication

# 🏁 Conclusion
This project demonstrates how MCP enables scalable AI systems by connecting agents with external tools and services using ADK. 


