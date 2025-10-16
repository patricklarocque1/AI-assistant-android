package com.aiassistant.chat.model

/**
 * Request model for Hugging Face API
 */
data class HuggingFaceRequest(
    val inputs: String,
    val parameters: Parameters = Parameters()
) {
    data class Parameters(
        val max_new_tokens: Int = 250,
        val temperature: Float = 0.7f,
        val top_p: Float = 0.95f,
        val return_full_text: Boolean = false
    )
}

/**
 * Response model from Hugging Face API
 */
data class HuggingFaceResponse(
    val generated_text: String? = null,
    val error: String? = null
)
