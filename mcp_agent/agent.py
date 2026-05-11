import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParameters

load_dotenv()

MAPS_API_KEY = os.getenv("MAPS_API_KEY")
MAPS_MCP_URL = "https://mapstools.googleapis.com/v1/mcp"

maps_toolset = McpToolset(
    connection_parameters=StreamableHTTPConnectionParameters(
        base_url=MAPS_MCP_URL,
        headers={"Authorization": f"Bearer {MAPS_API_KEY}"},
    )
)

root_agent = LlmAgent(
    name="root_agent",
    description="An agent that can use the MCP tools to answer questions about locations and directions.",
    tools=maps_toolset.get_tools(),
    instructions=(
        "You are a helpful assistant that can answer questions about locations and directions using the MCP tools. "
    )
)