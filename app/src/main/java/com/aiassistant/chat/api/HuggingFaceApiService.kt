package com.aiassistant.chat.api

import com.aiassistant.chat.model.HuggingFaceRequest
import com.aiassistant.chat.model.HuggingFaceResponse
import retrofit2.Response
import retrofit2.http.*

/**
 * Retrofit service interface for Hugging Face API and Local Server
 */
interface HuggingFaceApiService {
    
    /**
     * Query the Hugging Face inference API
     * @param authorization Bearer token with API key
     * @param request The request containing inputs and parameters
     * @return List of responses from the model
     */
    @POST("models/microsoft/DialoGPT-medium")
    suspend fun query(
        @Header("Authorization") authorization: String,
        @Body request: HuggingFaceRequest
    ): List<HuggingFaceResponse>

    /**
     * Get server configuration (Local server endpoint)
     */
    @GET("config")
    suspend fun getConfig(): Response<Map<String, Any>>

    /**
     * Update server configuration (Local server endpoint)
     */
    @POST("config")
    suspend fun updateConfig(@Body config: Map<String, Any>): Response<Map<String, Any>>

    /**
     * Get system information (Local server endpoint)
     */
    @GET("system")
    suspend fun getSystemInfo(): Response<Map<String, Any>>

    /**
     * Restart server (Local server endpoint)
     */
    @POST("restart")
    suspend fun restartServer(): Response<Map<String, Any>>
}
