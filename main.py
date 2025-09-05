from mcp.server.fastmcp import FastMCP
import requests
import os

# Get configuration from environment variables
MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("MCP_PORT", "8001"))

# Create an MCP server
mcp = FastMCP("Menu MCP", host=MCP_HOST, port=MCP_PORT)

@mcp.tool()
def get_menu():
    """
    Fetch the restaurant menu from the local API and return it as JSON.
    """
    try:
        response = requests.get("http://localhost:5000/api/menu")
        response.raise_for_status()  # raise error for 4xx/5xx responses
        return response.json()       # return JSON result
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(f"Menu MCP is running on {MCP_HOST}:{MCP_PORT}")
    mcp.run(transport="streamable-http")
