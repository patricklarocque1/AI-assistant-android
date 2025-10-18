# Remote Server Management

## Overview

The Android AI Assistant app now includes a comprehensive remote management interface that allows you to configure and control your Ubuntu PC's AI server directly from your Android device. No more SSH or manual file editing required!

## Features

### 🎮 Full Remote Control
- **View Server Configuration**: See all current settings in real-time
- **Update Settings Remotely**: Change AI models, performance settings, and more
- **Monitor System Resources**: Check CPU, RAM, GPU usage, and uptime
- **Restart Server**: Apply configuration changes with a single tap

### 🔧 Configuration Management

#### AI Model Selection
- Switch between different AI models instantly
- Popular models pre-configured:
  - **Qwen/Qwen3-0.6B** - Fast and lightweight (default)
  - **meta-llama/Llama-3.2-1B-Instruct** - Better quality responses
  - **microsoft/DialoGPT-medium** - Conversational AI specialist
  - **Gensyn/Qwen2.5-0.5B-Instruct** - Very fast responses
  - Custom model support

#### Model Storage Management
- View current cache directory
- Change storage location remotely
- Examples:
  - `/home/username/ai-models`
  - `/mnt/ssd/models`
  - `~/Desktop/AI-Models`

#### Performance Optimization
- **GPU Acceleration**: Toggle GPU usage on/off
- **8-bit Quantization**: Reduce memory by 50%
- **4-bit Quantization**: Reduce memory by 75%
- Real-time GPU detection and information

#### Generation Settings
- **Max Length**: Control response length (10-500 tokens)
- **Temperature**: Adjust creativity (0.1-2.0)
- **Top P**: Fine-tune response quality (0.1-1.0)

### 📊 System Monitoring

View real-time server statistics:
- **Uptime**: How long the server has been running
- **CPU Usage**: Current processor load percentage
- **Memory**: RAM usage and total available
- **GPU Memory**: VRAM usage (if GPU enabled)
- **Model Status**: Whether model is loaded
- **Device Info**: CPU/GPU being used

## Setup

### 1. Prerequisites

**On your Ubuntu PC:**
```bash
cd local_ai_server

# Install required dependencies
pip install psutil
# or reinstall all dependencies
pip install -r requirements.txt
```

### 2. Start the Server

```bash
cd local_ai_server
./start.sh
```

The server will:
1. Load the AI model
2. Start Flask server on port 5000
3. Create ngrok tunnel
4. Display the ngrok URL

### 3. Configure Android App

1. Open the app
2. Tap Settings (⚙️ icon)
3. Enable "Use Local Server"
4. Enter your ngrok URL
5. Tap "Test Connection"
6. Tap "Save"

### 4. Access Remote Management

1. In Settings, tap **"Manage Server Configuration"**
2. The app will load current server configuration
3. Make your desired changes
4. Tap **"Save Config"** to apply changes
5. Tap **"Restart Server"** to activate new settings

## How It Works

### API Endpoints

The server exposes several management endpoints:

#### GET `/config`
Retrieves current server configuration:
```json
{
  "model_name": "Qwen/Qwen3-0.6B",
  "model_cache_dir": "/home/username/ai-models",
  "use_gpu": true,
  "load_in_8bit": false,
  "load_in_4bit": false,
  "default_max_length": 100,
  "default_temperature": 0.8,
  "default_top_p": 0.9,
  "cuda_available": true,
  "gpu_name": "NVIDIA GeForce GTX 1080",
  "model_loaded": true
}
```

#### POST `/config`
Updates server configuration:
```json
{
  "model_name": "meta-llama/Llama-3.2-1B-Instruct",
  "use_gpu": true,
  "load_in_8bit": true,
  "default_temperature": 0.9
}
```

Response:
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "updated_fields": ["model_name", "use_gpu", "load_in_8bit", "default_temperature"],
  "note": "Restart the server for changes to take effect"
}
```

#### GET `/system`
Retrieves system information:
```json
{
  "uptime_seconds": 3600,
  "cpu_percent": 45.2,
  "memory_total_gb": 16.0,
  "memory_used_gb": 8.3,
  "memory_percent": 51.9,
  "gpu_memory_used_gb": 2.1,
  "gpu_memory_total_gb": 8.0,
  "model_loaded": true,
  "device": "cuda:0"
}
```

#### POST `/restart`
Requests server restart:
```json
{
  "success": true,
  "message": "Restart signal sent",
  "note": "Server will restart if managed by a process supervisor"
}
```

## User Interface

### Server Configuration Screen

The Android app provides an intuitive UI with four main sections:

#### 1. System Information Card
- Real-time system stats
- Model status
- Uptime display
- Resource usage meters

#### 2. Model Configuration Card
- Current model display
- "Change Model" button with popular options
- Cache directory management
- HuggingFace token status

#### 3. Performance Settings Card
- GPU toggle switch
- 8-bit quantization toggle
- 4-bit quantization toggle
- GPU detection indicator

#### 4. Generation Settings Card
- Max Length slider (10-500)
- Temperature slider (0.1-2.0)
- Top P slider (0.1-1.0)
- Real-time value display

### Action Buttons

- **Save Config**: Writes changes to server's `.env` file
- **Restart Server**: Triggers server restart to apply changes
- **Refresh**: Reloads current configuration from server

## Use Cases

### Scenario 1: Switch AI Models
**Problem**: You want to try a different AI model without SSHing into your PC.

**Solution**:
1. Open app → Settings → "Manage Server Configuration"
2. Tap "Change Model" in Model Configuration section
3. Select "meta-llama/Llama-3.2-1B-Instruct"
4. Tap "Save Config"
5. Tap "Restart Server"
6. Wait for restart (20-30 seconds)
7. Return to chat and test new model

### Scenario 2: Enable GPU for Faster Responses
**Problem**: Your server is using CPU, but you have a GPU available.

**Solution**:
1. Open Server Configuration screen
2. In Performance Settings, toggle "Use GPU" ON
3. Tap "Save Config"
4. Tap "Restart Server"
5. Check System Information to confirm GPU usage

### Scenario 3: Reduce Memory Usage
**Problem**: Server is using too much RAM.

**Solution**:
1. Open Server Configuration screen
2. In Performance Settings, enable "8-bit Quantization"
3. Memory usage will drop by ~50%
4. Tap "Save Config" → "Restart Server"
5. Monitor Memory in System Information

### Scenario 4: Adjust Response Length
**Problem**: AI responses are too long or too short.

**Solution**:
1. Open Server Configuration screen
2. In Generation Settings, adjust "Max Length" slider
3. Lower value = shorter responses (faster)
4. Higher value = longer responses (more detailed)
5. Tap "Save Config"
6. No restart needed for generation settings

### Scenario 5: Organize Models on SSD
**Problem**: You want to store models on a fast SSD instead of HDD.

**Solution**:
1. Open Server Configuration screen
2. Tap "Change Cache Dir" in Model Configuration
3. Enter: `/mnt/ssd/ai-models`
4. Tap "Apply"
5. Tap "Save Config" → "Restart Server"
6. Models will download to new location

## Best Practices

### 1. Test Before Saving
- Change settings one at a time
- Test thoroughly before making more changes
- Keep note of what works best

### 2. Monitor Resources
- Check System Information regularly
- Watch for high CPU/Memory usage
- Adjust settings if system is struggling

### 3. Model Selection
- Start with smaller models (0.5-1B parameters)
- Test quality vs. speed trade-offs
- Use quantization if memory is limited

### 4. Restart Timing
- Save multiple changes before restarting
- Restart during low-usage times
- Wait for full restart (20-30 seconds)

### 5. Backup Configuration
The `.env` file is auto-updated. To backup:
```bash
cp local_ai_server/.env local_ai_server/.env.backup
```

## Security Considerations

### Network Security
- **Ngrok**: Provides secure HTTPS tunnel
- **Local Network**: All traffic encrypted via TLS
- **No Exposed Ports**: No port forwarding required

### Configuration Safety
- Changes written to `.env` file with backup comments
- Original values preserved in comments
- Easy to revert if needed

### Access Control
- Only accessible via ngrok URL (not public)
- Ngrok URLs are private and unique
- Can regenerate URL anytime by restarting ngrok

## Troubleshooting

### Problem: Can't Connect to Server Configuration

**Symptoms**:
- "Failed to load configuration" error
- Connection timeout

**Solutions**:
1. Check ngrok URL is correct in Settings
2. Test basic connection first ("Test Connection" button)
3. Ensure server is running (`./status.sh`)
4. Check server logs for errors
5. Restart server if needed

### Problem: Changes Don't Take Effect

**Symptoms**:
- Configuration saved but model unchanged
- Settings revert after restart

**Solutions**:
1. Always tap "Restart Server" after saving
2. Wait 20-30 seconds for full restart
3. Refresh configuration to verify
4. Check `.env` file manually if needed:
   ```bash
   cat local_ai_server/.env
   ```

### Problem: Server Won't Restart

**Symptoms**:
- Restart button doesn't work
- Server remains on old configuration

**Solutions**:
1. The restart endpoint needs process manager support
2. Manual restart is required:
   ```bash
   cd local_ai_server
   ./stop.sh
   ./start.sh
   ```
3. Consider using systemd or supervisor for auto-restart

### Problem: GPU Not Detected

**Symptoms**:
- "GPU: Not available" in System Information
- GPU toggle disabled

**Solutions**:
1. Check CUDA installation on Ubuntu:
   ```bash
   nvidia-smi
   ```
2. Ensure PyTorch has CUDA support:
   ```bash
   python -c "import torch; print(torch.cuda.is_available())"
   ```
3. Reinstall PyTorch with CUDA if needed

### Problem: Model Download Fails

**Symptoms**:
- Server crashes after model change
- "Failed to load model" error

**Solutions**:
1. Check internet connection on Ubuntu PC
2. Verify model name is correct
3. For gated models, ensure HF_TOKEN is set
4. Check disk space in cache directory
5. Try smaller model first to test

## Advanced Features

### Custom Model Support

To use models not in the preset list:

1. In Model Configuration, tap "Change Model"
2. Select "Custom"
3. Enter full HuggingFace model path:
   - Example: `tiiuae/falcon-7b-instruct`
   - Example: `stabilityai/stablelm-2-1_6b`
4. Save and restart

### Monitoring Script

Create a monitoring script to track changes:

```bash
#!/bin/bash
# monitor_config.sh

while true; do
    echo "=== $(date) ==="
    curl -s http://localhost:5000/system | jq '.'
    sleep 60
done
```

Usage:
```bash
chmod +x monitor_config.sh
./monitor_config.sh > server_monitor.log &
```

### Automatic Backup

Add to your crontab for daily backups:
```bash
0 2 * * * cp ~/local_ai_server/.env ~/local_ai_server/.env.backup.$(date +\%Y\%m\%d)
```

## Performance Optimization Tips

### For Fast Responses
```
Model: Qwen3-0.6B or Qwen2.5-0.5B
GPU: Enabled
Quantization: 8-bit or 4-bit
Max Length: 60-80 tokens
Temperature: 0.7-0.8
```

### For High Quality
```
Model: Llama-3.2-1B-Instruct
GPU: Enabled
Quantization: None or 8-bit
Max Length: 100-200 tokens
Temperature: 0.8-0.9
```

### For Low Memory
```
Model: Qwen3-0.6B
GPU: Optional
Quantization: 4-bit (required)
Max Length: 60-80 tokens
```

### For Conversation
```
Model: DialoGPT-medium
GPU: Enabled
Quantization: 8-bit
Max Length: 80-100 tokens
Temperature: 0.8-0.9
Top P: 0.9-0.95
```

## Future Enhancements

Potential additions in future versions:

1. **Multi-Model Support**: Load multiple models simultaneously
2. **Automatic Restart**: Server auto-restarts on config change
3. **Performance Graphs**: Historical CPU/Memory/GPU charts
4. **Model Preloading**: Download models in background
5. **Configuration Profiles**: Save/load preset configurations
6. **Batch Operations**: Update multiple settings at once
7. **Remote Logs**: View server logs in app
8. **Health Alerts**: Notifications for server issues

## Conclusion

The Remote Server Management feature transforms your Android AI Assistant into a complete control center for your Ubuntu AI server. No more command-line configuration or SSH sessions—everything is accessible from your phone with an intuitive, user-friendly interface.

Whether you're experimenting with different models, optimizing performance, or monitoring system resources, the remote management interface gives you full control at your fingertips.

## See Also

- [LOCAL_SERVER_SETUP.md](LOCAL_SERVER_SETUP.md) - Initial server setup
- [LOCAL_MODEL_STORAGE.md](LOCAL_MODEL_STORAGE.md) - Model storage management
- [ANDROID_STUDIO_SETUP.md](ANDROID_STUDIO_SETUP.md) - Android app development
- [API_SETUP.md](API_SETUP.md) - API configuration details
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - General troubleshooting guide
