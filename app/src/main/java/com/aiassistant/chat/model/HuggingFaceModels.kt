package com.aiassistant.chat.model

/**
 * Request model for Hugging Face API
 */
data class HuggingFaceRequest(
    val inputs: String,
    val parameters: Parameters = Parameters()
) {
    data class Parameters(
        val max_new_tokens: Int = 100,
        val temperature: Float = 0.8f,
        val top_p: Float = 0.9f,
        val return_full_text: Boolean = false,
        val do_sample: Boolean = true,
        val pad_token_id: Int = 50256
    )
}

/**
 * Response model from Hugging Face API
 */
data class HuggingFaceResponse(
    val generated_text: String? = null,
    val error: String? = null
)
