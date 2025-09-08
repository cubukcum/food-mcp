from mcp.server.fastmcp import FastMCP
import requests
import os
import json

# Get configuration from environment variables
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8001"))
JWT_TOKEN_URL = os.getenv("JWT_TOKEN_URL", "http://localhost:5000/auth/token")
MENU_API_URL = os.getenv("MENU_API_URL", "http://localhost:5000/api/menu")

# Create an MCP server
mcp = FastMCP("Menu MCP", host=MCP_HOST, port=MCP_PORT)

def get_jwt_token():
    """
    Get JWT token from the authentication endpoint.
    Returns the token string or None if failed.
    """
    try:
        # You may need to adjust this based on your API requirements
        # Some APIs require credentials in the request body or headers
        response = requests.post(JWT_TOKEN_URL)
        response.raise_for_status()
        
        # Assuming the response contains a 'token' field
        # Adjust this based on your API's response format
        token_data = response.json()
        return token_data.get('token') or token_data.get('access_token')
        
    except requests.exceptions.RequestException as e:
        print(f"Error getting JWT token: {e}")
        return None

def get_menu_with_token(token):
    """
    Get menu using the JWT token.
    Returns the menu data or None if failed.
    """
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(MENU_API_URL, headers=headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error getting menu with token: {e}")
        return None

@mcp.tool()
def get_menu():
    """
    Fetch the restaurant menu using JWT authentication.
    First gets a JWT token, then uses it to fetch the menu.
    """
    # Step 1: Get JWT token
    token = get_jwt_token()
    if not token:
        return {"error": "Failed to obtain JWT token"}
    
    # Step 2: Get menu using the token
    menu_data = get_menu_with_token(token)
    if menu_data is None:
        return {"error": "Failed to fetch menu with JWT token"}
    
    return menu_data

if __name__ == "__main__":
    print(f"Menu MCP is running on {MCP_HOST}:{MCP_PORT}")
    mcp.run(transport="streamable-http")
