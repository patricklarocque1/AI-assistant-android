package com.aiassistant.chat.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aiassistant.chat.model.ChatMessage
import com.aiassistant.chat.repository.ChatRepository
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
    
    init {
        // Add welcome message
        addMessage(ChatMessage(
            content = "Hello! I'm your AI assistant powered by Hugging Face. How can I help you today?",
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
     * Send a message to the AI assistant
     */
    fun sendMessage(content: String) {
        if (content.isBlank()) return
        
        val apiKeyValue = _apiKey.value
        if (apiKeyValue.isNullOrBlank()) {
            _error.value = "Please configure your Hugging Face API key first"
            return
        }
        
        // Add user message
        val userMessage = ChatMessage(content = content, isUser = true)
        addMessage(userMessage)
        
        // Clear any previous error
        _error.value = null
        _isLoading.value = true
        
        viewModelScope.launch {
            val result = repository.sendMessage(content, apiKeyValue)
            
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
        _messages.value = listOf(ChatMessage(
            content = "Hello! I'm your AI assistant powered by Hugging Face. How can I help you today?",
            isUser = false
        ))
        _error.value = null
    }
    
    /**
     * Clear error message
     */
    fun clearError() {
        _error.value = null
    }
}
