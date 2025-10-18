# 🤖 Local AI Model Hosting - Quick Reference

## What We Built

A complete local AI model hosting solution that lets you:
- Run AI models on your Ubuntu desktop
- Expose them via Ngrok (no port forwarding needed)
- Connect your Android app to your own AI model
- Use for FREE with unlimited requests!

## 📁 Project Structure

```
AI-assistant-android/
├── app/                                    # Android app
│   └── src/main/java/com/aiassistant/chat/
│       ├── api/
│       │   ├── HuggingFaceApiService.kt   # Original HF API
│       │   ├── LocalAiApiService.kt       # NEW: Local server API
│       │   └── LocalRetrofitClient.kt     # NEW: Local server client
│       └── model/
│           ├── HuggingFaceModels.kt       # Original models
│           └── LocalServerModels.kt       # NEW: Local server models
│
└── local_ai_server/                       # NEW: AI Server
    ├── ai_server.py                       # Main server application
    ├── requirements.txt                   # Python dependencies
    ├── setup.sh                           # Setup script
    ├── start.sh                           # Start script
    ├── test_server.py                     # Test script
    ├── .env.example                       # Configuration template
    └── README.md                          # Server documentation
```

## 🚀 Quick Start (5 Steps)

### 1️⃣ Get Ngrok Token
```
Visit: https://dashboard.ngrok.com/signup
Sign up → Copy your auth token
```

### 2️⃣ Setup Server
```bash
cd local_ai_server
./setup.sh
nano .env  # Add your Ngrok token
```

### 3️⃣ Start Server
```bash
./start.sh
```
Copy the Ngrok URL that appears (e.g., `https://abc123.ngrok.io`)

### 4️⃣ Test Server
```bash
# In new terminal
cd local_ai_server
source venv/bin/activate
python test_server.py
```

### 5️⃣ Update Android App
Add the Ngrok URL to your app settings and switch to "Local Server" mode.

## 📊 Model Recommendations

### Your PC Specs → Recommended Model

| RAM | GPU | Recommended Model | Size | Quality |
|-----|-----|------------------|------|---------|
| 4GB | No | `Gensyn/Qwen2.5-0.5B-Instruct` | 500MB | Good |
| 6-8GB | No | `Qwen/Qwen3-0.6B` | 600MB | Better |
| 8GB+ | No | `meta-llama/Llama-3.2-1B-Instruct` | 1.2GB | Great |
| 8GB+ | Yes | `Qwen/Qwen2.5-3B-Instruct` | 3GB | Excellent |
| 16GB+ | Yes | `Qwen/Qwen2.5-7B-Instruct` | 7GB | Amazing |
| 32GB+ | Yes | `meta-llama/Llama-3.1-8B-Instruct` | 8GB | Best |

Change model in `.env`:
```bash
MODEL_NAME=Qwen/Qwen3-0.6B
```

## 🔧 API Endpoints

### POST /chat
Send message, get AI response
```bash
curl -X POST https://your-url.ngrok.io/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### GET /health
Check if server is healthy
```bash
curl https://your-url.ngrok.io/health
```

### GET /models
Get loaded model info
```bash
curl https://your-url.ngrok.io/models
```

## 📱 Android App Integration

### Minimal Integration
Just update the base URL in your settings:
```kotlin
val localServerUrl = "https://your-ngrok-url.ngrok.io"
```

### Full Integration
Use the new classes provided:
- `LocalAiApiService.kt` - API interface
- `LocalRetrofitClient.kt` - Client setup
- `LocalServerModels.kt` - Data models

See `ANDROID_INTEGRATION.md` for detailed steps.

## 🎯 Common Commands

```bash
# Start server
cd local_ai_server && ./start.sh

# Stop server
Ctrl+C

# View logs
tail -f server.log

# Change model
nano .env  # Edit MODEL_NAME

# Update dependencies
pip install -r requirements.txt --upgrade

# Test connection
python test_server.py https://your-url.ngrok.io

# Run in background
nohup ./start.sh > server.log 2>&1 &
```

## 🐛 Troubleshooting

### Server won't start
```bash
cd local_ai_server
rm -rf venv
./setup.sh
```

### Out of memory
```bash
# Use smaller model
nano .env
MODEL_NAME=Gensyn/Qwen2.5-0.5B-Instruct
```

### Ngrok URL changes
- Normal on free plan (changes on restart)
- Solution: Get paid plan ($8/month) for permanent URL
- Or: Save URL in app settings, update when needed

### Android can't connect
- Verify server is running
- Check Ngrok URL is correct (copy exactly)
- Test URL in phone browser first
- Make sure phone has internet

## 💰 Cost Comparison

| Solution | Cost | Limits | Speed | Privacy |
|----------|------|--------|-------|---------|
| **Local Server** | FREE | None | Fast* | 100% |
| Hugging Face API | FREE tier | Rate limits | Medium | Shared |
| OpenAI API | $0.002/1K | Pay per use | Fast | Shared |

*Speed depends on your PC specs

## 📚 Documentation

- `LOCAL_SERVER_SETUP.md` - Detailed server setup guide
- `ANDROID_INTEGRATION.md` - Android app integration guide
- `local_ai_server/README.md` - Server features and usage
- `QUICKSTART.md` - General app quick start

## 🎓 Learning Resources

### Understanding the Components

1. **Flask** - Python web framework for the API
2. **Transformers** - Hugging Face library for AI models
3. **PyTorch** - Machine learning framework
4. **Ngrok** - Tunneling service for exposing local server
5. **Retrofit** - Android HTTP client

### Next Level

- Fine-tune a model for your specific use case
- Add conversation memory/context
- Implement streaming responses
- Create multiple model endpoints
- Add authentication/security

## 🤝 Contributing

Want to improve this? Ideas:
- [ ] Add model switching without restart
- [ ] Implement conversation history
- [ ] Add voice input/output
- [ ] Create web interface
- [ ] Support multiple concurrent users
- [ ] Add response streaming
- [ ] Implement model fine-tuning scripts

## ⚠️ Important Notes

1. **First run downloads model** - Takes 5-30 mins depending on model size
2. **Ngrok URL changes** - On free plan, URL changes when you restart
3. **Keep PC running** - Server only works when PC is on
4. **Internet required** - For Ngrok tunnel (not for local network)
5. **Privacy** - Your conversations stay on your PC!

## 🎉 What's Next?

Now that you have your local AI server:

1. **Test different models** - Try various sizes and see what works best
2. **Fine-tune** - Train model on your specific data
3. **Expand features** - Add image generation, speech, etc.
4. **Share** - Help others set up their own servers
5. **Build** - Create amazing AI-powered apps!

## 📞 Support

Having issues?
1. Check the troubleshooting sections in docs
2. Review server logs: `tail -f local_ai_server/server.log`
3. Test endpoints with `test_server.py`
4. Verify Ngrok is working: visit URL in browser

---

**Made with ❤️ for developers who want control over their AI** 🚀
