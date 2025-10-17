#!/bin/bash
# Quick start script for local AI server

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     Local AI Model Server - Quick Start                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "ai_server.py" ]; then
    echo "❌ Error: Must be run from local_ai_server directory"
    echo "   Run: cd local_ai_server && ./quick_start.sh"
    exit 1
fi

# Check if setup has been run
if [ ! -d "venv" ]; then
    echo "📦 First-time setup detected. Running setup..."
    echo ""
    ./setup.sh
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed!"
        exit 1
    fi
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "You need to configure your environment first."
    echo ""
    echo "1. Get a FREE Ngrok token:"
    echo "   → Visit: https://dashboard.ngrok.com/signup"
    echo ""
    echo "2. Create .env file:"
    cp .env.example .env
    echo "   ✅ Created .env from template"
    echo ""
    echo "3. Add your Ngrok token:"
    echo "   → Edit: nano .env"
    echo "   → Add: NGROK_AUTH_TOKEN=your_token_here"
    echo ""
    echo "4. (Optional) Choose a model:"
    echo "   → Default: Qwen/Qwen3-0.6B (good for most PCs)"
    echo "   → Faster: Gensyn/Qwen2.5-0.5B-Instruct"
    echo "   → Better: meta-llama/Llama-3.2-1B-Instruct"
    echo ""
    echo "Then run this script again!"
    exit 0
fi

# Check if Ngrok token is set
source .env
if [ -z "$NGROK_AUTH_TOKEN" ] || [ "$NGROK_AUTH_TOKEN" = "your_ngrok_auth_token_here" ]; then
    echo "⚠️  Ngrok token not configured!"
    echo ""
    echo "Please edit .env and add your Ngrok auth token:"
    echo "  nano .env"
    echo ""
    echo "Get a FREE token at: https://dashboard.ngrok.com/signup"
    exit 1
fi

# Check system resources
echo "🔍 Checking system resources..."
echo ""

# Check RAM
total_ram=$(free -g | awk '/^Mem:/{print $2}')
echo "   RAM: ${total_ram}GB"

if [ "$total_ram" -lt 4 ]; then
    echo "   ⚠️  Warning: Less than 4GB RAM detected"
    echo "      Consider using: MODEL_NAME=Gensyn/Qwen2.5-0.5B-Instruct"
fi

# Check GPU
if command -v nvidia-smi &> /dev/null; then
    gpu_name=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -n 1)
    echo "   GPU: $gpu_name ✅"
    echo "   💡 You can use larger models like Qwen/Qwen2.5-3B-Instruct"
else
    echo "   GPU: Not detected (will use CPU)"
    echo "   💡 Recommended: Qwen/Qwen3-0.6B or smaller"
fi

echo ""

# Show current model
echo "📦 Model Configuration:"
echo "   Model: ${MODEL_NAME:-Qwen/Qwen3-0.6B}"
echo ""

# Ask to continue
read -p "Ready to start the server? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "🚀 Starting server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⏳ First run will download the model (5-30 minutes)"
echo "📦 Models are cached for future runs"
echo ""
echo "🌐 Your Ngrok URL will be displayed when ready"
echo "📱 Copy that URL to your Android app settings"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the server
./start.sh
