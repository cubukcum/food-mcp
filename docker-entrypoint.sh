#!/bin/bash
set -e

echo "Starting Food MCP Server..."

# Activate the virtual environment created by uv
source .venv/bin/activate

# Check if MCPO mode is requested
if [ "$MCPO_MODE" = "true" ]; then
    echo "Starting in MCPO mode (HTTP endpoints)..."
    exec python main.py --mcpo
else
    echo "Starting in direct MCP mode..."
    exec python main.py
fi
