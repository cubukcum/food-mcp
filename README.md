# Food MCP Server

A Model Context Protocol (MCP) server that provides restaurant menu data through a simple API.

## Features

- MCP server running on port 8001
- Fake API server providing menu data on port 5000
- Dockerized setup for easy deployment

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and run the container
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### Using Docker directly

```bash
# Build the image
docker build -t food-mcp .

# Run the container
docker run -p 8001:8001 food-mcp
```

## API Endpoints

- **MCP Server**: `http://localhost:8001` - MCP protocol endpoints
- **Menu API**: `http://localhost:5000/api/menu` - Returns menu data

## MCP Tools

- `get_menu()` - Fetches the restaurant menu from the local API

## Development

The MCP server connects to a local fake API that provides hardcoded menu data. Both services run in the same container for simplicity.
