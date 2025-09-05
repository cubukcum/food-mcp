# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv for faster builds
RUN pip install uv && \
    uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY main.py ./

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose the port
EXPOSE 8001

# Set default environment variables
ENV MCP_HOST=0.0.0.0 \
    MCP_PORT=8001

# Run the application
CMD ["python", "main.py"]
