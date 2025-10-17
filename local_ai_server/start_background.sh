#!/bin/bash
# Run AI server in background

cd /home/patrick/AI-assistant-android/local_ai_server

echo "🚀 Starting AI Server in background..."

# Kill any existing server
pkill -f "python.*ai_server.py" 2>/dev/null

# Start in background
nohup bash -c "source venv/bin/activate && python ai_server.py" > server.log 2>&1 &

# Get the process ID
SERVER_PID=$!

echo "✅ Server started with PID: $SERVER_PID"
echo ""
echo "⏳ Waiting for server to initialize..."
sleep 8

# Check if it's still running
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server is running!"
    echo ""
    
    # Get the Ngrok URL
    if [ -f "ngrok_url.txt" ]; then
        URL=$(cat ngrok_url.txt)
        echo "🌐 Ngrok URL: $URL"
    else
        echo "📝 Check server.log for Ngrok URL"
    fi
    
    echo ""
    echo "📊 Commands:"
    echo "  • View logs:  tail -f $PWD/server.log"
    echo "  • Stop server: kill $SERVER_PID"
    echo "  • Test server: curl $URL/health"
else
    echo "❌ Server failed to start. Check server.log:"
    tail -20 server.log
fi
