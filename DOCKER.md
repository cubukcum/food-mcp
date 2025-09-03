# Docker Setup for Food MCP Server

This document explains how to dockerize and run the Food MCP server.

## Files Created

- `Dockerfile` - Main Docker configuration
- `docker-compose.yml` - Docker Compose configuration for easy deployment
- `docker-entrypoint.sh` - Entrypoint script for proper server startup
- `.dockerignore` - Files to exclude from Docker build context

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and run the container:**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode:**
   ```bash
   docker-compose up -d --build
   ```

3. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t food-mcp .
   ```

2. **Run the container:**
   ```bash
   docker run --name food-mcp-server food-mcp
   ```

3. **Run in detached mode:**
   ```bash
   docker run -d --name food-mcp-server food-mcp
   ```

## Configuration

### Network Access

The MCP server tries to connect to `http://localhost:5000/api/menu`. If your API is running on the host machine, you have several options:

1. **Use host networking (uncomment in docker-compose.yml):**
   ```yaml
   network_mode: "host"
   ```

2. **Use a custom network:**
   ```yaml
   networks:
     - mcp-network
   ```

3. **Use the host's IP address instead of localhost in your main.py**

### Environment Variables

You can set environment variables in the `docker-compose.yml` file:

```yaml
environment:
  - API_URL=http://your-api-host:5000/api/menu
  - PYTHONUNBUFFERED=1
```

## Development

### Building for Development

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### Viewing Logs

```bash
docker-compose logs -f food-mcp
```

### Accessing the Container

```bash
docker-compose exec food-mcp bash
```

## Troubleshooting

### Common Issues

1. **Connection refused to localhost:5000:**
   - Ensure your API server is running
   - Use host networking or update the API URL
   - Check if the API is accessible from the host

2. **Permission issues:**
   - The container runs as a non-root user for security
   - Check file permissions if mounting volumes

3. **Build failures:**
   - Ensure all dependencies are listed in `pyproject.toml`
   - Check that `uv.lock` is up to date

### Debugging

1. **Check container status:**
   ```bash
   docker-compose ps
   ```

2. **View container logs:**
   ```bash
   docker-compose logs food-mcp
   ```

3. **Access container shell:**
   ```bash
   docker-compose exec food-mcp bash
   ```

## Security Notes

- The container runs as a non-root user (`app`)
- Only necessary system packages are installed
- The `.dockerignore` file excludes sensitive files
- Consider using secrets management for production deployments

## Production Deployment

For production deployment, consider:

1. Using a proper secrets management system
2. Setting up proper logging and monitoring
3. Using a reverse proxy (nginx) if needed
4. Implementing health checks and auto-restart policies
5. Using multi-stage builds to reduce image size
