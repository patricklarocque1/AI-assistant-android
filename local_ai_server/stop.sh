#!/bin/bash
# Stop AI server

echo "🛑 Stopping AI Server..."

# Kill the server process
pkill -f "python.*ai_server.py"

# Kill ngrok process
pkill -f "ngrok"

if [ $? -eq 0 ]; then
    echo "✅ Server stopped successfully"
else
    echo "ℹ️  No server was running"
fi
