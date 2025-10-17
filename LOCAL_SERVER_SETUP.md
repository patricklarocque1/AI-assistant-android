# Complete Setup Guide: Local AI Model Server

This guide will help you set up your own AI model server on your Ubuntu desktop and connect it to your Android app.

## Overview

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────┐
│  Android App    │ ◄─────► │    Ngrok     │ ◄─────► │  Your PC    │
│  (Phone)        │         │   Tunnel     │         │  AI Server  │
└─────────────────┘         └──────────────┘         └─────────────┘
```

## Part 1: Server Setup

### Step 1: Get Ngrok Token

1. Go to https://dashboard.ngrok.com/signup
2. Sign up for a free account
3. Go to "Your Authtoken" section
4. Copy your authtoken

### Step 2: Run Setup Script

```bash
cd local_ai_server
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all required dependencies
- Create a .env configuration file

### Step 3: Configure Environment

Edit the `.env` file:
```bash
nano .env
```

Add your Ngrok token:
```
NGROK_AUTH_TOKEN=your_actual_token_here
```

You can also choose a different model (optional):
```
MODEL_NAME=Qwen/Qwen3-0.6B
```

### Step 4: Start the Server

```bash
./start.sh
```

The first run will download the AI model (this takes 5-15 minutes).

After starting, you'll see:
```
🌐 Ngrok tunnel started!
🔗 Public URL: https://abc123.ngrok.io
📱 Use this URL in your Android app: https://abc123.ngrok.io
```

**Copy this URL!** You'll need it for your Android app.

### Step 5: Test the Server

In a new terminal:
```bash
cd local_ai_server
source venv/bin/activate
python test_server.py
```

Or test with the Ngrok URL:
```bash
python test_server.py https://your-ngrok-url.ngrok.io
```

## Part 2: Android App Configuration

### Option A: Modify Code to Use Local Server

You can modify your Android app to use your local server instead of Hugging Face API.

#### Update RetrofitClient.kt

Change the base URL to use your Ngrok URL:

```kotlin
private const val BASE_URL = "https://your-ngrok-url.ngrok.io/"

object RetrofitClient {
    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
    
    val api: LocalAiApiService by lazy {
        retrofit.create(LocalAiApiService::class.java)
    }
}
```

#### Update API Service

Create a new API service for your local server:

```kotlin
interface LocalAiApiService {
    @POST("chat")
    suspend fun chat(@Body request: LocalChatRequest): LocalChatResponse
}

data class LocalChatRequest(
    val message: String,
    val max_length: Int = 512,
    val temperature: Float = 0.7f,
    val top_p: Float = 0.9f
)

data class LocalChatResponse(
    val response: String,
    val model: String,
    val device: String
)
```

### Option B: Add Configuration in Settings

Add a setting to switch between Hugging Face API and local server.

## Part 3: Model Selection Guide

Choose based on your PC specs:

### For PC without GPU (4-8GB RAM):
```
MODEL_NAME=Gensyn/Qwen2.5-0.5B-Instruct  # Fastest, smallest
MODEL_NAME=Qwen/Qwen3-0.6B               # Good balance (recommended)
MODEL_NAME=meta-llama/Llama-3.2-1B-Instruct  # Best quality for CPU
```

### For PC with GPU (8-16GB RAM):
```
MODEL_NAME=Qwen/Qwen2.5-3B-Instruct      # Excellent quality
MODEL_NAME=Qwen/Qwen2.5-7B-Instruct      # High quality
```

### For Powerful PC with GPU (16GB+ RAM):
```
MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct  # Very high quality
MODEL_NAME=openai/gpt-oss-20b            # Highest quality
```

## Troubleshooting

### Server won't start
```bash
# Check Python installation
python3 --version

# Reinstall dependencies
cd local_ai_server
rm -rf venv
./setup.sh
```

### Out of memory error
- Use a smaller model (0.5B or 0.6B)
- Close other applications
- Add swap space:
  ```bash
  sudo fallocate -l 4G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  ```

### Ngrok connection refused
- Check your internet connection
- Verify your Ngrok token is correct
- Try restarting the server

### Model downloading is slow
- Normal for first run (5-30 minutes depending on model size)
- Model is cached in `~/.cache/huggingface/` for future runs

### Android app can't connect
- Make sure you're using the HTTPS Ngrok URL
- Check that server is still running
- Verify firewall isn't blocking connections

## Advanced Usage

### Keep Server Running in Background

```bash
cd local_ai_server
nohup ./start.sh > server.log 2>&1 &
```

Check logs:
```bash
tail -f server.log
```

### Run on System Startup

Create systemd service:
```bash
sudo nano /etc/systemd/system/ai-server.service
```

Add:
```ini
[Unit]
Description=Local AI Model Server
After=network.target

[Service]
Type=simple
User=patrick
WorkingDirectory=/home/patrick/AI-assistant-android/local_ai_server
ExecStart=/home/patrick/AI-assistant-android/local_ai_server/start.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ai-server
sudo systemctl start ai-server
sudo systemctl status ai-server
```

### Monitor Performance

```bash
# Watch GPU usage (if you have NVIDIA GPU)
watch -n 1 nvidia-smi

# Watch CPU/Memory
htop
```

## Tips for Best Performance

1. **Use a GPU**: Even a budget GPU (GTX 1050/1060) dramatically improves inference speed
2. **Start with small models**: Test with 0.6B model, then upgrade if needed
3. **Adjust temperature**: Lower = more focused, Higher = more creative
4. **Keep Ngrok running**: Free plan requires server restart daily (URL changes)
5. **Consider Ngrok paid plan**: Get permanent URL ($8/month)

## Cost Comparison

### Your Local Server:
- ✅ **FREE** after initial setup
- ✅ Unlimited requests
- ✅ Full control over model
- ✅ Privacy (data stays local)
- ❌ Requires keeping PC running

### Hugging Face API:
- ✅ Always available
- ✅ No infrastructure needed
- ❌ Rate limits on free tier
- ❌ Costs money for heavy usage
- ❌ Data sent to external server

## Next Steps

1. ✅ Set up local server
2. ✅ Get Ngrok URL
3. ⬜ Update Android app to use local server
4. ⬜ Test end-to-end communication
5. ⬜ Experiment with different models
6. ⬜ Fine-tune model for your specific use case (advanced)

Need help? Check the README files or open an issue on GitHub!
