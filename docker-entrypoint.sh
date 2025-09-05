#!/bin/bash
set -e

echo "Starting Menu MCP Server..."

# Start the fake API in the background if it's not already running
if ! pgrep -f "fake_api.py" > /dev/null; then
    echo "Starting fake API server..."
    cd /app/fakeAPI
    python fake_api.py &
    cd /app
    sleep 2  # Give the API time to start
fi

# Start the MCP server
echo "Starting MCP server on port 8001..."
exec python main.py
