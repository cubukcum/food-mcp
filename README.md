# Food MCP Server

A Model Context Protocol (MCP) server that provides restaurant menu information through a simple API interface. Now supports both direct MCP integration and HTTP endpoints via MCPO for maximum compatibility.

## What is this?

This is an MCP server that connects to a restaurant API and provides menu information to AI applications like Claude Desktop, OpenWebUI, and other MCP-compatible tools. It can run in two modes:

- **Direct MCP Mode**: Traditional MCP server for Claude Desktop and other MCP clients
- **HTTP Mode**: Exposes MCP tools as OpenAPI-compatible HTTP endpoints via MCPO for OpenWebUI

## Features

- 🍽️ **Menu Integration**: Fetches restaurant menu from your API
- 🐳 **Dockerized**: Easy deployment with Docker and Docker Compose
- 🔌 **Dual Mode**: Works with both MCP clients and HTTP endpoints
- 🌐 **OpenWebUI Compatible**: HTTP endpoints for OpenWebUI integration
- 🛠️ **Easy Setup**: Simple configuration and deployment

## Quick Start

### Option 1: HTTP Endpoints (Recommended for OpenWebUI)

```bash
# Copy example configuration
cp config.example.json config.json
cp docker-compose.example.yml docker-compose.yml

# Start the server with HTTP endpoints
docker-compose up -d

# Verify it's running
docker-compose ps

# Check HTTP endpoints
curl http://localhost:8001/food-mcp
```

### Option 2: Direct MCP (For Claude Desktop)

```bash
# Start the server in MCP mode
docker-compose up -d

# Connect to Claude Desktop (see configuration below)
```

### Connect to Claude Desktop

1. Find your Claude Desktop config file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

2. Add this configuration:
   ```json
   {
     "mcpServers": {
       "food-mcp": {
         "command": "docker",
         "args": ["exec", "-i", "food-mcp-server", "python", "main.py"],
         "env": {}
       }
     }
   }
   ```

3. Restart Claude Desktop

4. Test it: Ask "What's on the menu today?" or "Get the restaurant menu"

### Connect to OpenWebUI

1. Open OpenWebUI > Settings > Tools
2. Add a connection: `http://localhost:8001/food-mcp`
3. Check available tools on the chat page

## Requirements

- Docker and Docker Compose
- Your restaurant API running on `localhost:5000` (or update the URL in `main.py`)

## Available Tools

- **`get_menu`**: Fetches the restaurant menu from your API

## Running Modes

### HTTP Mode (Default)
The server runs with HTTP endpoints exposed on port 8001:
- `http://localhost:8001/food-mcp` - Main endpoint for OpenWebUI
- `http://localhost:8001/health` - Health check endpoint

### Direct MCP Mode
For traditional MCP clients like Claude Desktop, the server runs without HTTP endpoints.

To switch modes, set the `MCPO_MODE` environment variable:
```bash
# HTTP mode (default)
MCPO_MODE=true docker-compose up -d

# Direct MCP mode
MCPO_MODE=false docker-compose up -d
```

## Documentation

- 📖 **[Quick Start Guide](QUICK_START.md)** - Get up and running in minutes
- 🔧 **[MCP Integration Guide](MCP_INTEGRATION.md)** - Detailed integration instructions
- 🐳 **[Docker Setup](DOCKER.md)** - Docker configuration and deployment
- 🧪 **[Test Client](test_mcp_client.py)** - Python client for testing

## Project Structure

```
foodMCP/
├── main.py                 # MCP server implementation
├── pyproject.toml          # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── docker-entrypoint.sh    # Container entrypoint
├── test_mcp_client.py      # Test client
├── claude_desktop_config.json  # Claude Desktop config
├── openwebui_config.yaml   # OpenWebUI config
└── docs/
    ├── QUICK_START.md      # Quick start guide
    ├── MCP_INTEGRATION.md  # Integration guide
    └── DOCKER.md           # Docker documentation
```

## Commands

```bash
# Start the server (HTTP mode by default)
docker-compose up -d

# Start in MCP mode
MCPO_MODE=false docker-compose up -d

# Stop the server
docker-compose down

# View logs
docker-compose logs -f

# Test the server
python test_mcp_client.py

# Test HTTP endpoints
curl http://localhost:8001/food-mcp
curl http://localhost:8001/health
```

## Troubleshooting

- **Container not running**: Run `docker-compose up -d`
- **API connection failed**: Ensure your restaurant API is running on `localhost:5000`
- **Tool not available**: Restart Claude Desktop after config changes
- **HTTP endpoints not working**: Check if port 8001 is exposed and MCPO_MODE=true
- **MCPO import error**: Ensure all dependencies are installed with `uv sync`

## License

This project is open source and available under the MIT License.
