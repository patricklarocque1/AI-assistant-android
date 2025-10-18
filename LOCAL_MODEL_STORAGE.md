# Local Model Storage Management Guide

This guide explains how to organize and manage AI models in a custom folder on your Ubuntu desktop.

## Overview

Instead of using Hugging Face's hosted API, you can:
1. **Store models locally** in a folder of your choice (e.g., `/home/user/ai-models/`)
2. **Manage models** with provided scripts
3. **Optimize performance** with GPU acceleration and quantization
4. **Access via ngrok** from your Android app

## Quick Start

### 1. Setup Custom Model Folder

```bash
cd local_ai_server
python manage_models.py setup
```

This will prompt you for a custom directory path. Examples:
- `/home/username/ai-models/`
- `/mnt/storage/ai-models/`
- `~/Desktop/AI-Models/`

### 2. Configure Your .env File

Edit `.env`:
```bash
nano .env
```

Key settings for local model management:

```ini
# Custom model storage location
MODEL_CACHE_DIR=/home/username/ai-models

# Choose your model
MODEL_NAME=Qwen/Qwen3-0.6B

# Your Hugging Face Pro token (for downloading gated models)
HF_TOKEN=hf_your_token_here

# Performance optimizations
USE_GPU=true
LOAD_IN_8BIT=false  # Set to true for 8-bit quantization (saves memory)
LOAD_IN_4BIT=false  # Set to true for 4-bit quantization (even more memory savings)
```

### 3. First Run - Model Download

When you first start the server, it will:
1. Create your custom model folder if it doesn't exist
2. Download the selected model to that folder
3. Cache it for future use (no re-downloading)

```bash
./start.sh
```

**First time**: 5-15 minutes (downloading model)  
**Subsequent runs**: 10-30 seconds (loading from cache)

## Model Management

### List Models

See what models are stored in your cache:

```bash
python manage_models.py list
```

Output example:
```
📁 Model cache directory: /home/user/ai-models

📦 Models in cache:
======================================================================
  • Qwen/Qwen3-0.6B
    Size: 1.23 GB
    Path: /home/user/ai-models/hub/models--Qwen--Qwen3-0.6B

  • microsoft/DialoGPT-medium
    Size: 0.87 GB
    Path: /home/user/ai-models/hub/models--microsoft--DialoGPT-medium
======================================================================
```

### View Configuration

Check your current setup:

```bash
python manage_models.py config
```

### Clear Cache

Remove all downloaded models (to free up space):

```bash
python manage_models.py clear
```

⚠️ **Warning**: This deletes all models. You'll need to re-download them.

## Folder Structure

Your custom model folder will look like this:

```
/home/username/ai-models/
├── hub/
│   ├── models--Qwen--Qwen3-0.6B/
│   │   ├── snapshots/
│   │   │   └── abc123.../
│   │   │       ├── config.json
│   │   │       ├── model.safetensors
│   │   │       └── tokenizer.json
│   ├── models--microsoft--DialoGPT-medium/
│   └── models--meta-llama--Llama-3.2-1B-Instruct/
└── .locks/
```

## Switching Models

To use a different model:

1. **Edit .env**:
   ```ini
   MODEL_NAME=microsoft/DialoGPT-medium
   ```

2. **Restart server**:
   ```bash
   ./stop.sh
   ./start.sh
   ```

If the model isn't in your cache, it will be downloaded automatically.

## Recommended Models for Different Use Cases

### For Conversation (Best for chat apps)
```ini
MODEL_NAME=microsoft/DialoGPT-medium  # 0.9 GB
# or
MODEL_NAME=Qwen/Qwen3-0.6B            # 1.2 GB
```

### For Code Assistance
```ini
MODEL_NAME=Qwen/Qwen2.5-Coder-0.5B-Instruct  # 1.0 GB
```

### For General Purpose (Larger, better quality)
```ini
MODEL_NAME=meta-llama/Llama-3.2-1B-Instruct  # 2.5 GB (requires HF Pro)
```

## Performance Optimization

### GPU Acceleration

If you have an NVIDIA GPU with CUDA:

```ini
USE_GPU=true
```

This provides **5-10x faster** generation.

### Memory Optimization (Quantization)

For systems with limited RAM:

**8-bit quantization** (half memory usage):
```ini
LOAD_IN_8BIT=true
```

**4-bit quantization** (quarter memory usage):
```ini
LOAD_IN_4BIT=true
```

⚠️ Requires `bitsandbytes` package:
```bash
pip install bitsandbytes
```

### Memory Requirements

| Configuration | Example Model | RAM Needed |
|--------------|---------------|------------|
| Full precision (CPU) | Qwen3-0.6B | ~2-3 GB |
| Full precision (GPU) | Qwen3-0.6B | ~1.5 GB VRAM |
| 8-bit (GPU) | Qwen3-0.6B | ~0.8 GB VRAM |
| 4-bit (GPU) | Qwen3-0.6B | ~0.4 GB VRAM |

## Using Pre-Downloaded Models

If you already have models downloaded elsewhere:

1. **Find your current cache**:
   ```bash
   python manage_models.py config
   ```

2. **Move/copy models** to your custom folder:
   ```bash
   cp -r ~/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B \
         /home/username/ai-models/hub/
   ```

3. **Update .env** to point to your folder:
   ```ini
   MODEL_CACHE_DIR=/home/username/ai-models
   ```

4. **Start server** - it will use the existing model!

## Advanced: Multiple Model Configurations

Create different .env files for different setups:

**.env.fast** (small, fast model):
```ini
MODEL_NAME=Qwen/Qwen3-0.6B
LOAD_IN_4BIT=true
```

**.env.quality** (larger, better quality):
```ini
MODEL_NAME=meta-llama/Llama-3.2-1B-Instruct
USE_GPU=true
```

Use them:
```bash
cp .env.fast .env && ./start.sh
# or
cp .env.quality .env && ./start.sh
```

## Troubleshooting

### Model not downloading

**Check**:
1. Internet connection
2. HF_TOKEN is set (for gated models)
3. Disk space available

**Solution**:
```bash
python manage_models.py config  # Verify settings
df -h  # Check disk space
```

### Out of memory

**Solutions**:
1. Use quantization:
   ```ini
   LOAD_IN_8BIT=true
   ```
2. Choose smaller model:
   ```ini
   MODEL_NAME=Qwen/Qwen3-0.6B
   ```
3. Close other applications

### Model loading slow

**Optimizations**:
1. Use SSD for model storage (not HDD)
2. Enable GPU:
   ```ini
   USE_GPU=true
   ```
3. Use quantization to reduce load time

### Can't find custom folder

**Check**:
```bash
python manage_models.py config
```

**Fix .env**:
```ini
# Use absolute path
MODEL_CACHE_DIR=/home/username/ai-models

# Or expand ~ manually
MODEL_CACHE_DIR=/home/actualusername/ai-models
```

## Hugging Face Pro Subscription Benefits

With Hugging Face Pro, you get:

1. **Access to gated models**:
   - Llama 3.2
   - Mistral models
   - Other restricted models

2. **Faster downloads** (priority servers)

3. **More API rate limits** (when using hosted API)

To use Pro features:
```ini
# Add your Pro token
HF_TOKEN=hf_your_pro_token_here
```

## Backup and Restore

### Backup your models

```bash
tar -czf ai-models-backup.tar.gz /home/username/ai-models/
```

### Restore models

```bash
tar -xzf ai-models-backup.tar.gz -C /
```

## Integration with Android App

The Android app is already configured to work with local servers. Just:

1. **Start your server** with ngrok:
   ```bash
   ./start.sh
   ```

2. **Copy the ngrok URL** from output:
   ```
   🔗 Public URL: https://abc123.ngrok.io
   ```

3. **Configure in Android app**:
   - Open Settings (⚙️)
   - Enable "Use Local Server"
   - Paste the ngrok URL
   - Test connection

The app will now use YOUR local models instead of Hugging Face API!

## Next Steps

1. **Experiment with models**: Try different models for different tasks
2. **Optimize performance**: Enable GPU, try quantization
3. **Monitor usage**: Check `python manage_models.py config` regularly
4. **Share models**: Use same cache folder for multiple projects

## Related Documentation

- **LOCAL_SERVER_SETUP.md**: Complete server setup guide
- **LOCAL_AI_QUICK_REFERENCE.md**: Quick reference commands
- **COMMUNICATION_OPTIMIZATION.md**: Performance tuning
- **API_SETUP.md**: Android app configuration

---

**Questions or issues?** Check the troubleshooting section or open a GitHub issue.
