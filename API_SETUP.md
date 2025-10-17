# Hugging Face API Connection Guide

This guide explains how to set up and test the Hugging Face API connection in the AI Assistant app.

## Overview

The app uses the **Hugging Face Inference API** to communicate with AI models. The current implementation uses:
- **Model**: `mistralai/Mistral-7B-Instruct-v0.2`
- **Authentication**: Bearer token (API key)
- **Endpoint**: `https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2`

## API Authentication

### Token-Based Authentication (Bearer Token)

The app already implements proper token authentication:

```kotlin
// In ChatRepository.kt
val response = apiService.query(
    authorization = "Bearer $apiKey",
    request = request
)
```

The API key is:
1. Stored in the app's ViewModel (in-memory only)
2. Sent with each request as: `Authorization: Bearer YOUR_API_KEY`
3. Not persisted to disk for security

## Getting Your API Key

### Step 1: Create Hugging Face Account
1. Visit [huggingface.co](https://huggingface.co/)
2. Click **"Sign Up"** in the top right
3. Create account with email or OAuth (GitHub/Google)
4. Verify your email address

### Step 2: Generate Access Token
1. Log in to Hugging Face
2. Click your **profile picture** → **Settings**
3. Navigate to **"Access Tokens"** in the left sidebar
4. Click **"New token"** button
5. Configure token:
   - **Name**: `AI Assistant App` (or any name)
   - **Role**: Select **"Read"** (sufficient for inference)
   - **Repositories**: Leave default (all)
6. Click **"Generate token"**
7. **IMPORTANT**: Copy the token immediately (you won't see it again!)

### Token Format
Your token will look like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- Starts with `hf_`
- 32+ alphanumeric characters
- Keep it secret and secure

## Configure API Key in App

### Using the App UI (Recommended)

1. **Launch the app** on your device/emulator
2. **Tap Settings icon (⚙️)** in the top-right corner
3. **Enter API Key**:
   - Tap the "API Key" field
   - Paste your Hugging Face token
   - The field is password-masked for security
4. **Save**: Tap "Save API Key" button
5. **Navigate back** to chat screen using back arrow

### Programmatic Configuration (For Development)

For testing, you can set a default API key in the ViewModel:

```kotlin
// In ChatViewModel.kt - ONLY FOR TESTING, REMOVE BEFORE PRODUCTION
init {
    // WARNING: Never commit real API keys to version control
    _apiKey.value = "hf_your_token_here" // FOR TESTING ONLY
}
```

**⚠️ Security Warning**: Never commit real API keys to Git!

## Testing the Connection

### Test 1: Basic Message

1. Open the app
2. Type: `"Hello!"`
3. Tap Send (➤)
4. **Expected result**:
   - Loading indicator appears
   - AI responds within 5-10 seconds
   - Response appears in gray bubble

**If successful**: Connection is working! ✅

### Test 2: Model Loading

Sometimes models need time to "warm up":

1. Send: `"What is artificial intelligence?"`
2. If you get **"Model is loading"** error:
   - This is normal for first request
   - Wait 20-30 seconds
   - Try again
   - Model should respond now

### Test 3: Complex Query

Test the AI's capabilities:

```
Write a haiku about coding
```

**Expected**: AI generates a creative haiku response

### Test 4: Error Handling

Test with invalid API key:

1. Go to Settings
2. Enter: `invalid_key_12345`
3. Save and try to send a message
4. **Expected**: Error message displayed

This confirms error handling works correctly.

## Troubleshooting API Issues

### Error: "Please configure your Hugging Face API key first"

**Cause**: No API key set  
**Solution**:
1. Go to Settings (⚙️)
2. Enter your API key
3. Tap "Save API Key"

### Error: "Failed to get response"

**Possible causes**:
1. **Invalid API token**
   - Verify token is correct
   - Check for extra spaces
   - Generate new token if needed

2. **Network connectivity**
   - Check device has internet
   - Try on WiFi instead of mobile data
   - Check firewall/proxy settings

3. **API rate limits**
   - Free tier: 30 requests per hour
   - Wait and try again later
   - Consider upgrading to paid tier

### Error: "Model is loading"

**Cause**: Model container is starting up  
**Solution**:
- Wait 20-30 seconds
- Try again
- This only happens after periods of inactivity

### Error: "Unauthorized" or "401"

**Cause**: Invalid or expired API token  
**Solution**:
1. Go to Hugging Face Settings
2. Check if token is still active
3. Generate new token if needed
4. Update in app Settings

### Error: "Service Unavailable" or "503"

**Cause**: Hugging Face service is down or overloaded  
**Solution**:
- Check [status.huggingface.co](https://status.huggingface.co/)
- Wait and retry
- Try different time of day

### Slow Responses

**Possible causes**:
1. **Cold start**: First request takes longer
2. **Network speed**: Slow internet connection
3. **Model complexity**: Mistral-7B is a large model

**Solutions**:
- Wait patiently (can take 10-30 seconds)
- Use faster internet connection
- Consider smaller models for faster responses

## API Request Details

### Request Structure

```json
{
  "inputs": "Your message here",
  "parameters": {
    "max_new_tokens": 250,
    "temperature": 0.7,
    "top_p": 0.95,
    "return_full_text": false
  }
}
```

### Parameters Explained

- **max_new_tokens** (250): Maximum length of response
- **temperature** (0.7): Creativity (0=deterministic, 1=creative)
- **top_p** (0.95): Nucleus sampling threshold
- **return_full_text** (false): Only return generated text

### Customizing Parameters

Edit `HuggingFaceModels.kt`:

```kotlin
data class Parameters(
    val max_new_tokens: Int = 500,  // Longer responses
    val temperature: Float = 0.9f,   // More creative
    val top_p: Float = 0.95f,
    val return_full_text: Boolean = false
)
```

## Using Different Models

### Change the Model

Edit `HuggingFaceApiService.kt`:

```kotlin
@POST("models/YOUR_MODEL_HERE")
suspend fun query(...)
```

### Recommended Models

**Fast & Efficient**:
- `google/flan-t5-large` - Fast, good for simple tasks
- `microsoft/DialoGPT-medium` - Conversational

**High Quality**:
- `mistralai/Mistral-7B-Instruct-v0.2` - Current (best balance)
- `meta-llama/Llama-2-7b-chat-hf` - Requires approval

**Check model cards**: [huggingface.co/models](https://huggingface.co/models?pipeline_tag=text-generation)

## Rate Limits

### Free Tier
- **30 requests/hour** per model
- Rate limit resets every hour
- Shared across all your apps

### Pro Tier ($9/month)
- **Higher rate limits**
- Priority access
- Faster inference

### Enterprise
- Custom limits
- Dedicated endpoints
- SLA guarantees

## Security Best Practices

### ✅ Do:
- Store API key in app memory only (current implementation)
- Use HTTPS for all requests (already configured)
- Prompt user to enter their own API key
- Clear API key when app closes
- Use environment variables for development

### ❌ Don't:
- Hardcode API keys in source code
- Commit API keys to Git
- Share API keys publicly
- Store in SharedPreferences (unencrypted)
- Log API keys to console

## Monitoring API Usage

### Check Your Usage
1. Log in to [huggingface.co](https://huggingface.co/)
2. Go to **Settings → Billing**
3. View API usage statistics
4. Monitor rate limit consumption

### App-Level Monitoring

Add logging to track API calls:

```kotlin
// In ChatRepository.kt
Log.d("API", "Sending request to Hugging Face")
val response = apiService.query(...)
Log.d("API", "Received response: ${response.size} items")
```

## Advanced Configuration

### Custom Headers

Add custom headers in `RetrofitClient.kt`:

```kotlin
private val okHttpClient = OkHttpClient.Builder()
    .addInterceptor { chain ->
        val request = chain.request().newBuilder()
            .addHeader("X-App-Version", "1.0")
            .addHeader("X-Platform", "Android")
            .build()
        chain.proceed(request)
    }
    .build()
```

### Timeout Configuration

Already configured in `RetrofitClient.kt`:

```kotlin
.connectTimeout(30, TimeUnit.SECONDS)
.readTimeout(30, TimeUnit.SECONDS)
.writeTimeout(30, TimeUnit.SECONDS)
```

Increase if experiencing timeouts:
```kotlin
.readTimeout(60, TimeUnit.SECONDS)  // For slower models
```

## Getting Help

### Official Resources
- [Hugging Face Docs](https://huggingface.co/docs/api-inference/)
- [Inference API Reference](https://huggingface.co/docs/api-inference/detailed_parameters)
- [Status Page](https://status.huggingface.co/)

### Community Support
- [Hugging Face Forums](https://discuss.huggingface.co/)
- [Discord Community](https://hf.co/join/discord)

### Project-Specific
- Check **ARCHITECTURE.md** for code structure
- See **QUICKSTART.md** for usage guide
- Review **TROUBLESHOOTING.md** for common issues
- Open GitHub issue for bugs

---

**Quick Reference**: 
- API Endpoint: `https://api-inference.huggingface.co/`
- Auth Type: Bearer Token
- Header: `Authorization: Bearer YOUR_TOKEN`
- Free Tier: 30 requests/hour
- Model: Mistral-7B-Instruct-v0.2
