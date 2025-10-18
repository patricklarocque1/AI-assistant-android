#!/bin/bash
# Start script for Local AI Server

echo "=================================================="
echo "Starting Local AI Model Server"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your Ngrok token before running again!"
    exit 1
fi

# Start the server
echo ""
echo "Starting AI server..."
echo "=================================================="
python ai_server.py
