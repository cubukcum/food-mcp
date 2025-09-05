# Docker Deployment Guide

This guide explains how to dockerize and deploy the Food MCP Server.

## Prerequisites

- Docker Engine 20.10+ 
- Docker Compose 2.0+
- Git (to clone the repository)

## Quick Start

### 1. Build and Run with Docker Compose (Recommended)

```bash
# Copy environment variables
cp env.example .env

# Edit .env file if needed (optional)
# nano .env

# Build and start the service
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

### 2. Build and Run with Docker

```bash
# Build the image
docker build -t food-mcp .

# Run the container
docker run -d \
  --name food-mcp-server \
  -p 8001:8001 \
  -e MCP_HOST=0.0.0.0 \
  -e MCP_PORT=8001 \
  food-mcp
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_HOST` | `0.0.0.0` | Host address to bind the server |
| `MCP_PORT` | `8001` | Port number for the MCP server |

### Custom Configuration

1. Copy `env.example` to `.env`:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` file with your preferred settings:
   ```bash
   MCP_HOST=0.0.0.0
   MCP_PORT=8001
   ```

## Docker Commands

### Basic Operations

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up --build
```

### Container Management

```bash
# List running containers
docker ps

# View container logs
docker logs food-mcp-server

# Execute commands in container
docker exec -it food-mcp-server bash

# Stop container
docker stop food-mcp-server

# Remove container
docker rm food-mcp-server
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi food-mcp

# Clean up unused images
docker image prune
```

## Health Check

The container includes a built-in health check that verifies the MCP server is responding:

```bash
# Check container health
docker ps

# View health check logs
docker inspect food-mcp-server | grep -A 10 Health
```

## Production Deployment

### Security Considerations

1. **Non-root user**: The container runs as a non-root user for security
2. **Resource limits**: Set appropriate memory and CPU limits
3. **Network isolation**: Use Docker networks for service communication
4. **Secrets management**: Use Docker secrets or external secret management

### Scaling

```bash
# Scale the service (if needed)
docker-compose up --scale food-mcp=3
```

### Monitoring

```bash
# View resource usage
docker stats food-mcp-server

# View detailed container info
docker inspect food-mcp-server
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Check what's using the port
   netstat -tulpn | grep :8001
   
   # Use a different port
   MCP_PORT=8002 docker-compose up
   ```

2. **Container won't start**:
   ```bash
   # Check logs
   docker-compose logs food-mcp
   
   # Check container status
   docker ps -a
   ```

3. **Build failures**:
   ```bash
   # Clean build
   docker-compose build --no-cache
   
   # Remove old images
   docker system prune -a
   ```

### Debug Mode

```bash
# Run with debug output
docker-compose up --build --force-recreate

# Access container shell
docker exec -it food-mcp-server bash
```

## Development

### Local Development with Docker

```bash
# Mount source code for development
docker run -d \
  --name food-mcp-dev \
  -p 8001:8001 \
  -v $(pwd)/main.py:/app/main.py \
  food-mcp
```

### Testing

```bash
# Test the MCP server
curl http://localhost:8001/health

# Test with MCP client
# (Use your preferred MCP client to connect to localhost:8001)
```

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes (if any)
docker-compose down -v

# Complete cleanup
docker system prune -a
```
