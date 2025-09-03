# MCP Server Integration Guide

This guide explains how to integrate your dockerized Yemek MCP server with various MCP-compatible applications.

## Prerequisites

1. **Docker and Docker Compose installed**
2. **Your MCP server running** (see `DOCKER.md` for setup)
3. **Your restaurant API running** on `localhost:5000` (or update the URL in `main.py`)

## Quick Start

First, ensure your MCP server is running:

```bash
docker-compose up -d
```

## Integration with Different Applications

### 1. Claude Desktop

Claude Desktop is the easiest way to test your MCP server.

#### Setup Steps:

1. **Find Claude Desktop config location:**
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux:** `~/.config/claude/claude_desktop_config.json`

2. **Create or edit the config file:**
   ```json
   {
     "mcpServers": {
       "yemek-mcp": {
         "command": "docker",
         "args": [
           "exec",
           "-i",
           "yemek-mcp-server",
           "python",
           "main.py"
         ],
         "env": {}
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test the integration:**
   - Open Claude Desktop
   - You should see your MCP server available
   - Try asking: "What's on the menu today?" or "Get the restaurant menu"

### 2. OpenWebUI

OpenWebUI supports MCP servers through configuration.

#### Setup Steps:

1. **Create MCP server configuration:**
   ```yaml
   # In your OpenWebUI config or environment
   MCP_SERVERS: |
     yemek-mcp:
       command: docker
       args: ["exec", "-i", "yemek-mcp-server", "python", "main.py"]
       env: {}
   ```

2. **Alternative: Direct Python execution:**
   ```yaml
   MCP_SERVERS: |
     yemek-mcp:
       command: python
       args: ["/path/to/your/project/main.py"]
       env:
         PYTHONPATH: "/path/to/your/project"
   ```

3. **Restart OpenWebUI**

### 3. Cline (VS Code Extension)

Cline is a VS Code extension that supports MCP servers.

#### Setup Steps:

1. **Install Cline extension in VS Code**

2. **Configure MCP server in Cline settings:**
   ```json
   {
     "cline.mcpServers": {
       "yemek-mcp": {
         "command": "docker",
         "args": ["exec", "-i", "yemek-mcp-server", "python", "main.py"],
         "env": {}
       }
     }
   }
   ```

### 4. MCP Inspector (Testing Tool)

Use MCP Inspector to test your server directly.

#### Setup Steps:

1. **Install MCP Inspector:**
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

2. **Run the inspector:**
   ```bash
   mcp-inspector docker exec -i yemek-mcp-server python main.py
   ```

3. **Test your tools in the web interface**

### 5. Custom MCP Client

You can also create your own MCP client using the MCP SDK.

#### Example Python Client:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Connect to your MCP server
    server_params = StdioServerParameters(
        command="docker",
        args=["exec", "-i", "yemek-mcp-server", "python", "main.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", tools)
            
            # Call the get_menu tool
            result = await session.call_tool("get_menu", {})
            print("Menu result:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration Options

### Environment Variables

You can customize your MCP server behavior using environment variables:

```yaml
# In docker-compose.yml
environment:
  - API_URL=http://your-api-host:5000/api/menu
  - PYTHONUNBUFFERED=1
  - LOG_LEVEL=INFO
```

### Network Configuration

If your API is not on localhost, update the connection:

1. **Update main.py:**
   ```python
   import os
   
   API_URL = os.getenv('API_URL', 'http://localhost:5000/api/menu')
   
   @mcp.tool()
   def get_menu():
       try:
           response = requests.get(API_URL)
           # ... rest of the function
   ```

2. **Set environment variable in docker-compose.yml:**
   ```yaml
   environment:
     - API_URL=http://your-api-host:5000/api/menu
   ```

## Testing Your Integration

### 1. Basic Functionality Test

```bash
# Test if your MCP server is responding
docker exec yemek-mcp-server python -c "
import requests
try:
    response = requests.get('http://localhost:5000/api/menu')
    print('API Response:', response.status_code)
    print('Menu:', response.json())
except Exception as e:
    print('Error:', e)
"
```

### 2. MCP Protocol Test

```bash
# Test MCP protocol directly
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | \
docker exec -i yemek-mcp-server python main.py
```

### 3. Integration Test with Claude Desktop

1. Open Claude Desktop
2. Ask: "What tools do you have available?"
3. You should see your `get_menu` tool listed
4. Ask: "Can you get the restaurant menu?"
5. The tool should be called and return the menu data

## Troubleshooting

### Common Issues

1. **"MCP server not found"**
   - Ensure Docker container is running: `docker-compose ps`
   - Check container logs: `docker-compose logs yemek-mcp`

2. **"Connection refused to localhost:5000"**
   - Ensure your restaurant API is running
   - Use host networking in docker-compose.yml
   - Update API URL in main.py

3. **"Permission denied"**
   - Check file permissions in the container
   - Ensure the container user has proper access

4. **"Tool not available in Claude Desktop"**
   - Restart Claude Desktop after config changes
   - Check the config file syntax
   - Verify the Docker command is correct

### Debug Commands

```bash
# Check if container is running
docker-compose ps

# View container logs
docker-compose logs -f yemek-mcp

# Access container shell
docker-compose exec yemek-mcp bash

# Test MCP server directly
docker exec yemek-mcp-server python main.py

# Check if API is accessible from container
docker exec yemek-mcp-server curl http://localhost:5000/api/menu
```

## Advanced Configuration

### Multiple MCP Servers

You can run multiple MCP servers by creating additional services in docker-compose.yml:

```yaml
services:
  yemek-mcp:
    # ... existing config
  
  another-mcp:
    build: ./another-mcp-server
    container_name: another-mcp-server
    # ... config
```

### Production Deployment

For production use:

1. **Use proper secrets management**
2. **Set up monitoring and logging**
3. **Use a reverse proxy if needed**
4. **Implement proper health checks**
5. **Use container orchestration (Kubernetes, Docker Swarm)**

## Security Considerations

1. **Network isolation:** Use custom Docker networks
2. **API authentication:** Implement proper API authentication
3. **Container security:** Run as non-root user (already configured)
4. **Secrets management:** Use Docker secrets or external secret managers
5. **Access control:** Implement proper access controls for your MCP server
