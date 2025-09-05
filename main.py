from mcp.server.fastmcp import FastMCP
import requests

# Create an MCP server
mcp = FastMCP("Menu MCP", host="127.0.0.1", port=8001)

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
    print("Menu MCP is running on port 8001")
    mcp.run(transport="streamable-http")
