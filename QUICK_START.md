# Quick Start Guide - Using Your MCP Server

This guide will get you up and running with your food MCP server in just a few minutes.

## Prerequisites

- Docker and Docker Compose installed
- Your restaurant API running on `localhost:5000` (or update the URL in `main.py`)

## Step 1: Start Your MCP Server

```bash
# Start the MCP server in the background
docker-compose up -d

# Verify it's running
docker-compose ps
```

## Step 2: Choose Your Integration Method

### Option A: Claude Desktop (Easiest)

1. **Find your Claude Desktop config file:**
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux:** `~/.config/claude/claude_desktop_config.json`

2. **Copy the configuration:**
   ```json
   {
     "mcpServers": {
       "food-mcp": {
         "command": "docker",
         "args": [
           "exec",
           "-i",
           "food-mcp-server",
           "python",
           "main.py"
         ],
         "env": {}
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test it:**
   - Open Claude Desktop
   - Ask: "What tools do you have available?"
   - You should see `get_menu` tool listed
   - Ask: "Get the restaurant menu"

### Option B: OpenWebUI

1. **Set environment variable:**
   ```bash
   export MCP_SERVERS='{"food-mcp": {"command": "docker", "args": ["exec", "-i", "food-mcp-server", "python", "main.py"], "env": {}}}'
   ```

2. **Restart OpenWebUI**

3. **Test in the web interface**

### Option C: Test with Python Client

1. **Install MCP library:**
   ```bash
   pip install mcp
   ```

2. **Run the test client:**
   ```bash
   python test_mcp_client.py
   ```

## Step 3: Verify Everything Works

### Check Container Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f food-mcp
```

### Test API Connection
```bash
# Test if your restaurant API is accessible
curl http://localhost:5000/api/menu
```

### Test MCP Server Directly
```bash
# Test the MCP server
docker exec food-mcp-server python main.py
```

## Troubleshooting

### "Container not found"
```bash
# Make sure you're in the right directory
cd /path/to/your/foodMCP

# Start the container
docker-compose up -d
```

### "Connection refused to localhost:5000"
- Make sure your restaurant API is running
- If API is on a different host, update the URL in `main.py`
- Or use host networking in `docker-compose.yml`

### "Tool not available in Claude Desktop"
- Restart Claude Desktop after config changes
- Check the config file syntax
- Verify Docker container is running

## Next Steps

Once everything is working:

1. **Read the full documentation:** `MCP_INTEGRATION.md`
2. **Customize your server:** Add more tools or modify existing ones
3. **Deploy to production:** See production deployment section in `DOCKER.md`

## Quick Commands Reference

```bash
# Start server
docker-compose up -d

# Stop server
docker-compose down

# View logs
docker-compose logs -f

# Restart server
docker-compose restart

# Update and rebuild
docker-compose up -d --build

# Access container shell
docker-compose exec food-mcp bash
```

## Need Help?

- Check the logs: `docker-compose logs food-mcp`
- Test the API: `curl http://localhost:5000/api/menu`
- Run the test client: `python test_mcp_client.py`
- Read the full documentation in `MCP_INTEGRATION.md`
