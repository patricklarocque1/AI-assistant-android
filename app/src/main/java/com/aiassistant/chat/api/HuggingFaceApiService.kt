package com.aiassistant.chat.api

import com.aiassistant.chat.model.HuggingFaceRequest
import com.aiassistant.chat.model.HuggingFaceResponse
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST

/**
 * Retrofit service interface for Hugging Face API
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
}
