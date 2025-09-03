# Yemek MCP Server

A Model Context Protocol (MCP) server that provides restaurant menu information through a simple API interface.

## What is this?

This is an MCP server that connects to a restaurant API and provides menu information to AI applications like Claude Desktop, OpenWebUI, and other MCP-compatible tools.

## Features

- 🍽️ **Menu Integration**: Fetches restaurant menu from your API
- 🐳 **Dockerized**: Easy deployment with Docker and Docker Compose
- 🔌 **MCP Compatible**: Works with Claude Desktop, OpenWebUI, and other MCP clients
- 🛠️ **Easy Setup**: Simple configuration and deployment

## Quick Start

### 1. Start the MCP Server

```bash
# Start the server
docker-compose up -d

# Verify it's running
docker-compose ps
```

### 2. Connect to Claude Desktop

1. Find your Claude Desktop config file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

2. Add this configuration:
   ```json
   {
     "mcpServers": {
       "yemek-mcp": {
         "command": "docker",
         "args": ["exec", "-i", "yemek-mcp-server", "python", "main.py"],
         "env": {}
       }
     }
   }
   ```

3. Restart Claude Desktop

4. Test it: Ask "What's on the menu today?" or "Get the restaurant menu"

## Requirements

- Docker and Docker Compose
- Your restaurant API running on `localhost:5000` (or update the URL in `main.py`)

## Available Tools

- **`get_menu`**: Fetches the restaurant menu from your API

## Documentation

- 📖 **[Quick Start Guide](QUICK_START.md)** - Get up and running in minutes
- 🔧 **[MCP Integration Guide](MCP_INTEGRATION.md)** - Detailed integration instructions
- 🐳 **[Docker Setup](DOCKER.md)** - Docker configuration and deployment
- 🧪 **[Test Client](test_mcp_client.py)** - Python client for testing

## Project Structure

```
yemekMCP/
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
# Start the server
docker-compose up -d

# Stop the server
docker-compose down

# View logs
docker-compose logs -f

# Test the server
python test_mcp_client.py
```

## Troubleshooting

- **Container not running**: Run `docker-compose up -d`
- **API connection failed**: Ensure your restaurant API is running on `localhost:5000`
- **Tool not available**: Restart Claude Desktop after config changes

## License

This project is open source and available under the MIT License.
