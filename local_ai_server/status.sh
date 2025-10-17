#!/bin/bash
# Check AI server status

cd /home/patrick/AI-assistant-android/local_ai_server

echo "📊 AI Server Status"
echo "===================="
echo ""

# Check if process is running
if pgrep -f "python.*ai_server.py" > /dev/null; then
    PID=$(pgrep -f "python.*ai_server.py")
    echo "✅ Server is RUNNING (PID: $PID)"
    echo ""
    
    # Check Ngrok URL
    if [ -f "ngrok_url.txt" ]; then
        URL=$(cat ngrok_url.txt)
        echo "🌐 Ngrok URL: $URL"
        echo ""
        
        # Test the endpoint
        echo "🧪 Testing /health endpoint..."
        curl -s "$URL/health" -m 5 | python3 -m json.tool 2>/dev/null || echo "⚠️  Could not reach server"
    else
        echo "⚠️  ngrok_url.txt not found"
    fi
    
    echo ""
    echo "📝 Recent logs:"
    echo "---------------"
    tail -10 server.log
    
else
    echo "❌ Server is NOT running"
    echo ""
    echo "Start it with: ./start_background.sh"
fi
