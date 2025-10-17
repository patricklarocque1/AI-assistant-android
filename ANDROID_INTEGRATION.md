# Android App Integration Guide

## Connecting Your Android App to Your Local AI Server

This guide explains how to integrate your Android app with your self-hosted AI model server.

## Prerequisites

1. Local AI server running (see `LOCAL_SERVER_SETUP.md`)
2. Ngrok URL from your server (e.g., `https://abc123.ngrok.io`)
3. Android app built and ready

## Integration Steps

### Step 1: Add New Model Classes

The following files have been created:
- `LocalServerModels.kt` - Data models for local server communication
- `LocalAiApiService.kt` - API interface for local server
- `LocalRetrofitClient.kt` - Retrofit client for local server

### Step 2: Update ChatRepository

Add support for both Hugging Face and local server:

```kotlin
class ChatRepository {
    private var useLocalServer = false
    private var localServerUrl = ""
    
    fun setServerConfig(useLocal: Boolean, url: String = "") {
        useLocalServer = useLocal
        localServerUrl = url
        
        if (useLocal && url.isNotEmpty()) {
            LocalRetrofitClient.initialize(url)
        }
    }
    
    suspend fun sendMessage(message: String): String {
        return if (useLocalServer) {
            sendToLocalServer(message)
        } else {
            sendToHuggingFace(message)
        }
    }
    
    private suspend fun sendToLocalServer(message: String): String {
        return try {
            val request = LocalChatRequest(
                message = message,
                maxLength = 512,
                temperature = 0.7f,
                topP = 0.9f
            )
            
            val response = LocalRetrofitClient.getApiService().chat(request)
            response.response
        } catch (e: Exception) {
            "Error: ${e.message}"
        }
    }
    
    private suspend fun sendToHuggingFace(message: String): String {
        // Your existing Hugging Face implementation
        // ...
    }
}
```

### Step 3: Add Server Configuration UI

Add to `SettingsScreen.kt`:

```kotlin
@Composable
fun ServerConfigurationSection(
    useLocalServer: Boolean,
    localServerUrl: String,
    onUseLocalServerChanged: (Boolean) -> Unit,
    onLocalServerUrlChanged: (String) -> Unit,
    onTestConnection: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Text(
            text = "Server Configuration",
            style = MaterialTheme.typography.titleLarge,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        // Toggle between Hugging Face and Local Server
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Use Local Server",
                modifier = Modifier.weight(1f)
            )
            Switch(
                checked = useLocalServer,
                onCheckedChange = onUseLocalServerChanged
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Server URL input (only shown if local server is enabled)
        if (useLocalServer) {
            OutlinedTextField(
                value = localServerUrl,
                onValueChange = onLocalServerUrlChanged,
                label = { Text("Local Server URL") },
                placeholder = { Text("https://your-ngrok-url.ngrok.io") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Uri
                )
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "Enter your Ngrok URL from the local server",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Test connection button
            Button(
                onClick = onTestConnection,
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(
                    imageVector = Icons.Default.PlayArrow,
                    contentDescription = null,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("Test Connection")
            }
        }
    }
}
```

### Step 4: Update ChatViewModel

Add server configuration handling:

```kotlin
class ChatViewModel : ViewModel() {
    private val repository = ChatRepository()
    
    private val _useLocalServer = MutableStateFlow(false)
    val useLocalServer: StateFlow<Boolean> = _useLocalServer
    
    private val _localServerUrl = MutableStateFlow("")
    val localServerUrl: StateFlow<String> = _localServerUrl
    
    fun setUseLocalServer(use: Boolean) {
        _useLocalServer.value = use
        updateServerConfig()
    }
    
    fun setLocalServerUrl(url: String) {
        _localServerUrl.value = url
        updateServerConfig()
    }
    
    private fun updateServerConfig() {
        repository.setServerConfig(
            useLocal = _useLocalServer.value,
            url = _localServerUrl.value
        )
    }
    
    fun testConnection() {
        viewModelScope.launch {
            try {
                val response = LocalRetrofitClient.getApiService().healthCheck()
                if (response.status == "healthy") {
                    // Show success message
                    _messages.value += ChatMessage(
                        text = "✅ Connected to local server! Model: ${response.device}",
                        isUser = false,
                        timestamp = System.currentTimeMillis()
                    )
                }
            } catch (e: Exception) {
                // Show error message
                _messages.value += ChatMessage(
                    text = "❌ Connection failed: ${e.message}",
                    isUser = false,
                    timestamp = System.currentTimeMillis()
                )
            }
        }
    }
}
```

### Step 5: Save Configuration

Use SharedPreferences or DataStore to persist settings:

```kotlin
// In your Application class or ViewModel
private fun saveServerConfig() {
    val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    prefs.edit().apply {
        putBoolean("use_local_server", useLocalServer)
        putString("local_server_url", localServerUrl)
        apply()
    }
}

private fun loadServerConfig() {
    val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    val useLocal = prefs.getBoolean("use_local_server", false)
    val url = prefs.getString("local_server_url", "") ?: ""
    
    if (useLocal && url.isNotEmpty()) {
        setUseLocalServer(true)
        setLocalServerUrl(url)
    }
}
```

## Testing

### 1. Test Server Connection

```kotlin
// In your app settings screen
Button(onClick = {
    viewModel.testConnection()
}) {
    Text("Test Connection")
}
```

### 2. Send Test Message

Once connected, send a message through the chat interface. You should see:
- Faster responses (if your PC is decent)
- Different response quality (depending on model)
- No rate limits!

### 3. Monitor Server

On your PC, watch the server logs:
```bash
cd local_ai_server
tail -f server.log
```

You'll see requests coming from your Android app!

## Troubleshooting

### Connection Timeout
- **Issue**: App can't connect to server
- **Solution**: 
  - Verify Ngrok URL is correct
  - Check server is running
  - Make sure phone has internet connection
  - Try accessing URL in phone's browser first

### SSL Certificate Errors
- **Issue**: SSL handshake failures
- **Solution**: Ngrok provides valid SSL certificates, but if issues persist:
  ```kotlin
  // Add to LocalRetrofitClient (NOT recommended for production)
  val trustAllCerts = object : X509TrustManager {
      override fun checkClientTrusted(chain: Array<X509Certificate>, authType: String) {}
      override fun checkServerTrusted(chain: Array<X509Certificate>, authType: String) {}
      override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
  }
  ```

### Slow Responses
- **Issue**: AI takes too long to respond
- **Solution**:
  - Use a smaller model on your server
  - Reduce `max_length` parameter
  - Consider getting a GPU for your PC

### Ngrok URL Changes
- **Issue**: URL changes every time you restart server
- **Solution**:
  - Save URL in app settings (don't hardcode)
  - Get Ngrok paid plan for permanent URL ($8/month)
  - Or set up dynamic DNS with port forwarding

## Advanced: Dynamic URL Updates

For automatic URL updates without manually entering Ngrok URL:

### Option 1: QR Code Scanning
1. Generate QR code with Ngrok URL on server startup
2. Scan QR code from Android app
3. Auto-configure server URL

### Option 2: Local Network Discovery
1. Use mDNS/Bonjour for local network discovery
2. Auto-detect server on same network
3. Fall back to Ngrok for remote access

### Option 3: Configuration Server
1. Host a simple config endpoint with permanent URL
2. Server updates its current Ngrok URL there
3. App fetches current URL from config endpoint

## Benefits of Local Server

✅ **Free & Unlimited**: No API costs or rate limits
✅ **Privacy**: Your conversations never leave your network
✅ **Customizable**: Choose any model, fine-tune for your needs
✅ **Fast**: Local processing can be faster than API calls
✅ **Offline**: Works without internet (if on same network)

## Next Steps

1. Implement the code changes above
2. Test connection from your Android app
3. Compare response quality with Hugging Face API
4. Experiment with different models
5. Consider fine-tuning a model for your specific use case

Happy coding! 🚀
