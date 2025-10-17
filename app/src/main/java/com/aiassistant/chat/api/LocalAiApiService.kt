package com.aiassistant.chat.api

import com.aiassistant.chat.model.LocalChatRequest
import com.aiassistant.chat.model.LocalChatResponse
import com.aiassistant.chat.model.ServerHealthResponse
import com.aiassistant.chat.model.ModelInfoResponse
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

/**
 * Retrofit service interface for Local AI Server
 * This connects to your self-hosted AI model via Ngrok
 */
interface LocalAiApiService {
    
    /**
     * Send a chat message to your local AI model
     * @param request The chat request containing the message
     * @return Response from your AI model
     */
    @POST("chat")
    suspend fun chat(
        @Body request: LocalChatRequest
    ): LocalChatResponse
    
    /**
     * Check server health status
     * @return Health status of the server
     */
    @GET("health")
    suspend fun healthCheck(): ServerHealthResponse
    
    /**
     * Get information about the loaded model
     * @return Model information
     */
    @GET("models")
    suspend fun getModelInfo(): ModelInfoResponse
}
