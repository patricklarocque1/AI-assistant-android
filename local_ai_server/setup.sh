#!/bin/bash
# Setup script for Local AI Server

echo "=================================================="
echo "Local AI Model Server Setup"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Install it with: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Ngrok token!"
    echo "   Get a free token at: https://dashboard.ngrok.com/signup"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "=================================================="
echo "Setup complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add your Ngrok auth token"
echo "3. Run the server: ./start.sh"
echo ""
