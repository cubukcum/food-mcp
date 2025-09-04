from mcp.server.fastmcp import FastMCP
import requests
import os
import json
import sys

# Create an MCP server
mcp = FastMCP("Menu MCP")

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

def run_mcp_server():
    """Run the MCP server directly"""
    print("Menu MCP is running")
    mcp.run()

def run_mcpo_server():
    """Run the MCPO server to expose HTTP endpoints"""
    try:
        import mcpo
        import uvicorn
        
        # Load configuration
        config_path = "config.json"
        if not os.path.exists(config_path):
            print(f"Configuration file {config_path} not found. Using default configuration.")
            config = {
                "mcpServers": {
                    "food-mcp": {
                        "command": "python",
                        "args": ["main.py"],
                        "env": {"PYTHONPATH": "/app"}
                    }
                },
                "server": {
                    "host": "0.0.0.0",
                    "port": 8001,
                    "log_level": "info"
                }
            }
        else:
            with open(config_path, 'r') as f:
                config = json.load(f)
        
        print("Starting MCPO server...")
        print(f"Server will be available at: http://{config['server']['host']}:{config['server']['port']}")
        print(f"Food MCP endpoint: http://{config['server']['host']}:{config['server']['port']}/food-mcp")
        
        # Start the MCPO server
        uvicorn.run(
            "mcpo.main:app",
            host=config['server']['host'],
            port=config['server']['port'],
            log_level=config['server']['log_level']
        )
    except ImportError:
        print("MCPO not available. Running MCP server directly.")
        run_mcp_server()

if __name__ == "__main__":
    # Check if we should run MCPO or direct MCP
    if len(sys.argv) > 1 and sys.argv[1] == "--mcpo":
        run_mcpo_server()
    else:
        run_mcp_server()