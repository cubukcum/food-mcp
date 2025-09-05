# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv (Python package manager)
RUN pip install uv

# Install dependencies using uv
RUN uv sync --frozen

# Copy application code and configuration
COPY main.py ./

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port for MCP server HTTP endpoints
EXPOSE 8001

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV API_URL=http://localhost:5000

# Create entrypoint script
COPY --chown=app:app docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

# Use entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
