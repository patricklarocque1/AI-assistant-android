# Local AI Model Server

This server hosts a Hugging Face AI model locally on your Ubuntu desktop and exposes it via Ngrok for your Android app to access.

## Features

- 🤖 Host any Hugging Face text-generation model locally
- 🌐 Automatic Ngrok tunnel setup
- 🔌 RESTful API compatible with your Android app
- 🚀 Easy to set up and use
- 💾 Runs on CPU or GPU (automatically detected)

## Quick Start

### 1. Install Dependencies

```bash
cd local_ai_server
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add:
- Your Ngrok auth token (get free token at https://dashboard.ngrok.com/signup)
- Choose your model (default: Qwen/Qwen3-0.6B)
- Optionally add HuggingFace token for gated models

### 3. Run the Server

```bash
python ai_server.py
```

The server will:
1. Download and load the AI model (first run takes longer)
2. Start the Flask server
3. Create an Ngrok tunnel
4. Display the public URL to use in your Android app

### 4. Update Your Android App

Copy the Ngrok URL from the terminal output and update your Android app to use it instead of the Hugging Face API.

## API Endpoints

### POST /chat
Send a chat message and get AI response

**Request:**
```json
{
  "message": "Hello, how are you?",
  "max_length": 512,
  "temperature": 0.7,
  "top_p": 0.9
}
```

**Response:**
```json
{
  "response": "I'm doing well, thank you!",
  "model": "Qwen/Qwen3-0.6B",
  "device": "cpu"
}
```

### GET /health
Check server health

### GET /models
Get information about the loaded model

## Recommended Models

### Small & Fast (Good for CPU)
- `Qwen/Qwen3-0.6B` - 600M parameters, fast inference
- `Gensyn/Qwen2.5-0.5B-Instruct` - 500M parameters, very fast
- `meta-llama/Llama-3.2-1B-Instruct` - 1B parameters, good quality

### Medium (Better with GPU)
- `Qwen/Qwen2.5-3B-Instruct` - 3B parameters, excellent quality
- `Qwen/Qwen2.5-7B-Instruct` - 7B parameters, high quality

### Large (Requires GPU & lots of RAM)
- `meta-llama/Llama-3.1-8B-Instruct` - 8B parameters, very high quality

## System Requirements

### Minimum:
- 4GB RAM (for 0.5B-1B models)
- 10GB disk space
- Ubuntu Desktop (or any Linux)

### Recommended:
- 8GB+ RAM (for 3B+ models)
- NVIDIA GPU with CUDA support (for faster inference)
- 20GB+ disk space

## Troubleshooting

### Out of Memory
- Use a smaller model (0.5B or 0.6B)
- Close other applications
- Consider upgrading RAM

### Slow Inference
- Use a smaller model
- Consider getting a GPU
- Reduce max_length in requests

### Ngrok Connection Issues
- Make sure you have a valid auth token
- Check your internet connection
- Try restarting the server

## Notes

- First run downloads the model (may take 5-30 minutes depending on model size)
- Models are cached in `~/.cache/huggingface/`
- Ngrok URL changes each time you restart (free plan)
- For production, consider using Ngrok paid plan for permanent URL
