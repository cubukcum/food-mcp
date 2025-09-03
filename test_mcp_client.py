#!/usr/bin/env python3
"""
Test client for the Yemek MCP Server
This script demonstrates how to connect to and use your MCP server programmatically.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict

# You can install this with: pip install mcp
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("MCP library not found. Install it with: pip install mcp")
    sys.exit(1)


class YemekMCPClient:
    """Client for interacting with the Yemek MCP Server"""
    
    def __init__(self, use_docker: bool = True):
        self.use_docker = use_docker
        if use_docker:
            self.server_params = StdioServerParameters(
                command="docker",
                args=["exec", "-i", "yemek-mcp-server", "python", "main.py"]
            )
        else:
            # Direct Python execution (adjust path as needed)
            self.server_params = StdioServerParameters(
                command="python",
                args=["main.py"]
            )
    
    async def connect(self):
        """Connect to the MCP server"""
        self.read, self.write = await stdio_client(self.server_params)
        self.session = ClientSession(self.read, self.write)
        await self.session.initialize()
        print("✅ Connected to Yemek MCP Server")
    
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if hasattr(self, 'session'):
            await self.session.close()
        print("✅ Disconnected from Yemek MCP Server")
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        tools = await self.session.list_tools()
        print(f"📋 Available tools: {len(tools.tools)}")
        for tool in tools.tools:
            print(f"  - {tool.name}: {tool.description}")
        return tools.tools
    
    async def get_menu(self) -> Dict[str, Any]:
        """Get the restaurant menu"""
        print("🍽️  Fetching restaurant menu...")
        try:
            result = await self.session.call_tool("get_menu", {})
            print("✅ Menu retrieved successfully")
            return result
        except Exception as e:
            print(f"❌ Error getting menu: {e}")
            return {"error": str(e)}
    
    async def test_connection(self) -> bool:
        """Test if the server is responding"""
        try:
            await self.list_tools()
            return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False


async def main():
    """Main test function"""
    print("🚀 Starting Yemek MCP Server Test")
    print("=" * 50)
    
    # Check if Docker container is running
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=yemek-mcp-server", "--format", "{{.Names}}"],
            capture_output=True, text=True, check=True
        )
        if "yemek-mcp-server" not in result.stdout:
            print("❌ Docker container 'yemek-mcp-server' is not running")
            print("   Start it with: docker-compose up -d")
            return
        print("✅ Docker container is running")
    except subprocess.CalledProcessError:
        print("❌ Docker not available or container not found")
        return
    
    # Create and test the client
    client = YemekMCPClient(use_docker=True)
    
    try:
        # Connect to the server
        await client.connect()
        
        # Test connection
        if not await client.test_connection():
            return
        
        # List available tools
        tools = await client.list_tools()
        
        # Test the get_menu tool
        menu_result = await client.get_menu()
        
        # Display results
        print("\n📊 Test Results:")
        print("=" * 30)
        print(f"Tools available: {len(tools)}")
        print(f"Menu result: {json.dumps(menu_result, indent=2)}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        await client.disconnect()
    
    print("\n✅ Test completed")


if __name__ == "__main__":
    asyncio.run(main())
