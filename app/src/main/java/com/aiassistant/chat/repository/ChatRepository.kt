package com.aiassistant.chat.repository

import com.aiassistant.chat.api.RetrofitClient
import com.aiassistant.chat.model.HuggingFaceRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Repository to handle data operations for chat functionality
 */
class ChatRepository {
    
    private val apiService = RetrofitClient.apiService
    
    /**
     * Send a message to the Hugging Face API and get a response
     * @param message The user's message
     * @param apiKey The Hugging Face API key
     * @return The AI's response text or null if error
     */
    suspend fun sendMessage(message: String, apiKey: String): Result<String> {
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
                        !generatedText.isNullOrBlank() -> Result.success(generatedText)
                        !errorText.isNullOrBlank() -> Result.failure(Exception(errorText))
                        else -> Result.failure(Exception("Empty response from API"))
                    }
                } else {
                    Result.failure(Exception("Empty response from API"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }
}
