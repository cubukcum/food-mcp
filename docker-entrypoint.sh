#!/bin/bash
set -e

echo "Starting Yemek MCP Server..."

# Activate the virtual environment created by uv
source .venv/bin/activate

# Run the MCP server
exec python main.py
