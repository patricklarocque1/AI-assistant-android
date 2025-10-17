package com.aiassistant.chat.model

import com.google.gson.annotations.SerializedName

/**
 * Request model for local AI server
 */
data class LocalChatRequest(
    @SerializedName("message")
    val message: String,
    
    @SerializedName("max_length")
    val maxLength: Int = 512,
    
    @SerializedName("temperature")
    val temperature: Float = 0.7f,
    
    @SerializedName("top_p")
    val topP: Float = 0.9f
)

/**
 * Response model from local AI server
 */
data class LocalChatResponse(
    @SerializedName("response")
    val response: String,
    
    @SerializedName("model")
    val model: String,
    
    @SerializedName("device")
    val device: String
)

/**
 * Server health check response
 */
data class ServerHealthResponse(
    @SerializedName("status")
    val status: String,
    
    @SerializedName("model_loaded")
    val modelLoaded: Boolean,
    
    @SerializedName("device")
    val device: String?
)

/**
 * Model information response
 */
data class ModelInfoResponse(
    @SerializedName("model_name")
    val modelName: String,
    
    @SerializedName("device")
    val device: String?,
    
    @SerializedName("model_loaded")
    val modelLoaded: Boolean
)

/**
 * Server configuration
 */
data class ServerConfig(
    val useLocalServer: Boolean = false,
    val localServerUrl: String = "",
    val huggingFaceApiKey: String = ""
)
