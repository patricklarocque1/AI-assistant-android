package com.aiassistant.chat.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aiassistant.chat.model.ChatMessage
import com.aiassistant.chat.repository.ChatRepository
import com.aiassistant.chat.model.GenerationConfig
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel for managing chat state and business logic
 */
class ChatViewModel : ViewModel() {
    
    private val repository = ChatRepository()
    
    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()
    
    private val _apiKey = MutableStateFlow<String?>(null)
    val apiKey: StateFlow<String?> = _apiKey.asStateFlow()
    
    // Local server configuration
    private val _useLocalServer = MutableStateFlow(false)
    val useLocalServer: StateFlow<Boolean> = _useLocalServer.asStateFlow()
    
    private val _localServerUrl = MutableStateFlow<String>("")
    val localServerUrl: StateFlow<String> = _localServerUrl.asStateFlow()
    
    private val _serverStatus = MutableStateFlow<String?>(null)
    val serverStatus: StateFlow<String?> = _serverStatus.asStateFlow()
    
    init {
        // Add welcome message
        updateWelcomeMessage()
    }
    
    private fun updateWelcomeMessage() {
        val serverType = if (_useLocalServer.value) "your local AI server" else "Hugging Face"
        _messages.value = listOf(ChatMessage(
            content = "Hello! I'm your AI assistant powered by $serverType. How can I help you today?",
            isUser = false
        ))
    }
    
    /**
     * Set the API key for Hugging Face
     */
    fun setApiKey(key: String) {
        _apiKey.value = key
    }
    
    /**
     * Configure to use local server
     */
    fun setUseLocalServer(use: Boolean) {
        _useLocalServer.value = use
        updateServerConfig()
        updateWelcomeMessage()
    }
    
    /**
     * Set local server URL
     */
    fun setLocalServerUrl(url: String) {
        _localServerUrl.value = url
        updateServerConfig()
    }
    
    /**
     * Update repository configuration
     */
    private fun updateServerConfig() {
        try {
            repository.setServerConfig(
                useLocal = _useLocalServer.value,
                url = _localServerUrl.value
            )
            _error.value = null
        } catch (e: Exception) {
            _error.value = e.message
        }
    }
    
    /**
     * Test local server connection
     */
    fun testLocalServerConnection() {
        if (_localServerUrl.value.isBlank()) {
            _serverStatus.value = "Please enter a server URL"
            return
        }
        
        viewModelScope.launch {
            _isLoading.value = true
            _serverStatus.value = "Testing connection..."
            
            try {
                repository.setServerConfig(
                    useLocal = true,
                    url = _localServerUrl.value
                )
                
                // Try to send a test message
                val result = repository.sendMessage("Hello", "")
                
                result.fold(
                    onSuccess = {
                        _serverStatus.value = "✅ Connected successfully!"
                        addMessage(ChatMessage(
                            content = "✅ Local server connection successful! You can now chat.",
                            isUser = false
                        ))
                    },
                    onFailure = { exception ->
                        _serverStatus.value = "❌ Connection failed: ${exception.message}"
                    }
                )
            } catch (e: Exception) {
                _serverStatus.value = "❌ Connection failed: ${e.message}"
            }
            
            _isLoading.value = false
        }
    }
    
    /**
     * Send a message to the AI assistant
     */
    fun sendMessage(content: String) {
        if (content.isBlank()) return

        // Check configuration based on server type
        if (!_useLocalServer.value) {
            val apiKeyValue = _apiKey.value
            if (apiKeyValue.isNullOrBlank()) {
                _error.value = "Please configure your Hugging Face API key first"
                return
            }
        } else {
            if (_localServerUrl.value.isBlank()) {
                _error.value = "Please configure your local server URL first"
                return
            }
        }

        // Add user message
        val userMessage = ChatMessage(content = content, isUser = true)
        addMessage(userMessage)

        // Clear any previous error and status
        _error.value = null
        _serverStatus.value = null
        _isLoading.value = true

        // Dynamic maxLength logic: short for short prompts, longer for complex
        val dynamicMaxLength = when {
            content.length <= 8 -> 32 // very short prompt, short response
            content.length <= 32 -> 64 // medium prompt
            else -> 128 // long prompt, allow more tokens
        }
        val genConfig = GenerationConfig(maxLength = dynamicMaxLength)

        viewModelScope.launch {
            val apiKeyValue = _apiKey.value ?: ""
            val result = repository.sendMessage(content, apiKeyValue, genConfig)

            result.fold(
                onSuccess = { response ->
                    addMessage(ChatMessage(content = response, isUser = false))
                    _error.value = null
                },
                onFailure = { exception ->
                    _error.value = exception.message ?: "Failed to get response"
                }
            )

            _isLoading.value = false
        }
    }
    
    /**
     * Add a message to the chat
     */
    private fun addMessage(message: ChatMessage) {
        _messages.value = _messages.value + message
    }
    
    /**
     * Clear all messages
     */
    fun clearMessages() {
        updateWelcomeMessage()
        _error.value = null
        _serverStatus.value = null
    }
    
    /**
     * Clear error message
     */
    fun clearError() {
        _error.value = null
    }
}
