package com.aiassistant.chat.repository

import com.aiassistant.chat.api.RetrofitClient
import com.aiassistant.chat.api.LocalRetrofitClient
import com.aiassistant.chat.model.HuggingFaceRequest
import com.aiassistant.chat.model.LocalChatRequest
import com.aiassistant.chat.model.GenerationConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import retrofit2.HttpException

/**
 * Repository to handle data operations for chat functionality
 * Supports both Hugging Face API and local AI server
 * Optimized for efficient communication
 */
class ChatRepository {
    private val apiService = RetrofitClient.apiService

    // Configuration for server selection
    private var useLocalServer = false
    private var localServerUrl: String? = null

    // Generation config (can be set from ViewModel)
    private var generationConfig: GenerationConfig = GenerationConfig()
    
    // Conversation context for better responses
    private val conversationHistory = mutableListOf<String>()
    private val maxHistorySize = 5 // Keep last 5 exchanges for context

    /**
     * Configure whether to use local server or Hugging Face API
     */
    fun setServerConfig(useLocal: Boolean, url: String? = null, config: GenerationConfig? = null) {
        useLocalServer = useLocal
        localServerUrl = url
        if (config != null) generationConfig = config

        if (useLocal && !url.isNullOrBlank()) {
            try {
                LocalRetrofitClient.initialize(url)
            } catch (e: Exception) {
                throw IllegalArgumentException("Failed to initialize local server: ${e.message}")
            }
        }
    }
    
    /**
     * Clear conversation history
     */
    fun clearHistory() {
        conversationHistory.clear()
    }

    /**
     * Send a message to the AI (either local server or Hugging Face)
     * @param message The user's message
     * @param apiKey The Hugging Face API key (not used for local server)
     * @param config Optional generation config (overrides default)
     * @return The AI's response text
     */
    suspend fun sendMessage(message: String, apiKey: String, config: GenerationConfig? = null): Result<String> {
        val genConfig = config ?: generationConfig
        
        // Build context-aware prompt
        val contextualPrompt = buildContextualPrompt(message)
        
        val result = if (useLocalServer && localServerUrl != null) {
            sendToLocalServer(contextualPrompt, genConfig)
        } else {
            sendToHuggingFace(contextualPrompt, apiKey)
        }
        
        // Update conversation history on success
        result.onSuccess { response ->
            conversationHistory.add("User: $message")
            conversationHistory.add("AI: $response")
            
            // Trim history to maintain performance
            while (conversationHistory.size > maxHistorySize * 2) {
                conversationHistory.removeAt(0)
                conversationHistory.removeAt(0)
            }
        }
        
        return result
    }
    
    /**
     * Build a prompt with conversation context for better responses
     */
    private fun buildContextualPrompt(message: String): String {
        return if (conversationHistory.isEmpty()) {
            message
        } else {
            // Include recent context (last 2 exchanges max for efficiency)
            val recentContext = conversationHistory.takeLast(4).joinToString("\n")
            "$recentContext\nUser: $message\nAI:"
        }
    }
    
    /**
     * Send a message to the local AI server
     */
    private suspend fun sendToLocalServer(message: String, config: GenerationConfig): Result<String> {
        return withContext(Dispatchers.IO) {
            try {
                if (!LocalRetrofitClient.isInitialized()) {
                    return@withContext Result.failure(Exception("Local server not initialized"))
                }

                val request = LocalChatRequest(
                    message = message,
                    maxLength = config.maxLength,
                    temperature = config.temperature,
                    topP = config.topP
                )

                val response = LocalRetrofitClient.getApiService().chat(request)
                
                // Clean up response
                val cleanedResponse = cleanupResponse(response.response, message)
                Result.success(cleanedResponse)

            } catch (e: HttpException) {
                val errorMessage = when (e.code()) {
                    404 -> "Local server endpoint not found. Is the server running?"
                    500 -> "Local server error. Check server logs."
                    503 -> "Local server is busy. Try again in a moment."
                    else -> "HTTP ${e.code()}: ${e.message()}"
                }
                Result.failure(Exception(errorMessage))
            } catch (e: Exception) {
                Result.failure(Exception("Failed to connect to local server: ${e.message}"))
            }
        }
    }
    
    /**
     * Send a message to the Hugging Face API and get a response
     * @param message The user's message
     * @param apiKey The Hugging Face API key
     * @return The AI's response text or null if error
     */
    private suspend fun sendToHuggingFace(message: String, apiKey: String): Result<String> {
        return withContext(Dispatchers.IO) {
            try {
                val request = HuggingFaceRequest(
                    inputs = message
                )
                val response = apiService.query(
                    authorization = "Bearer $apiKey",
                    request = request
                )
                
                if (response.isNotEmpty()) {
                    val generatedText = response[0].generated_text
                    val errorText = response[0].error
                    
                    when {
                        !generatedText.isNullOrBlank() -> {
                            val cleanedResponse = cleanupResponse(generatedText, message)
                            Result.success(cleanedResponse)
                        }
                        !errorText.isNullOrBlank() -> Result.failure(Exception("API Error: $errorText"))
                        else -> Result.failure(Exception("Empty response from API"))
                    }
                } else {
                    Result.failure(Exception("Empty response from API"))
                }
            } catch (e: HttpException) {
                val errorBody = e.response()?.errorBody()?.string()
                val errorMessage = when (e.code()) {
                    401 -> "Invalid API key. Please check your Hugging Face API key."
                    404 -> "Model not found. The DialoGPT-medium model may not be available."
                    429 -> "Rate limit exceeded. Please try again in a minute."
                    503 -> "Model is loading. This may take 20-30 seconds. Please try again."
                    else -> "HTTP ${e.code()}: ${e.message()}"
                }
                Result.failure(Exception("$errorMessage${if (errorBody != null) "\nDetails: $errorBody" else ""}"))
            } catch (e: Exception) {
                Result.failure(Exception("Network error: ${e.message}"))
            }
        }
    }
    
    /**
     * Clean up AI response to remove prompt repetition and improve quality
     */
    private fun cleanupResponse(response: String, originalPrompt: String): String {
        var cleaned = response.trim()
        
        // Remove the original prompt if it's repeated
        if (cleaned.startsWith(originalPrompt)) {
            cleaned = cleaned.substring(originalPrompt.length).trim()
        }
        
        // Remove "AI:" or "User:" prefixes if present
        cleaned = cleaned.removePrefix("AI:").removePrefix("User:").trim()
        
        // Remove excessive newlines
        cleaned = cleaned.replace(Regex("\n{3,}"), "\n\n")
        
        // Truncate if response is too long (safety measure)
        if (cleaned.length > 500) {
            cleaned = cleaned.take(500).trimEnd() + "..."
        }
        
        return cleaned.ifBlank { "I'm thinking... Could you rephrase that?" }
    }
}
