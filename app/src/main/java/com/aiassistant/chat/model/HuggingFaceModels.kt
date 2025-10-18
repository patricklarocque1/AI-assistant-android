package com.aiassistant.chat.model

/**
 * Request model for Hugging Face API
 * Optimized parameters for efficient conversational AI
 */
data class HuggingFaceRequest(
    val inputs: String,
    val parameters: Parameters = Parameters()
) {
    data class Parameters(
        // Optimized for faster responses with good quality
        val max_new_tokens: Int = 60,          // Reduced for quicker responses
        val temperature: Float = 0.8f,         // Balanced creativity
        val top_p: Float = 0.9f,               // Nucleus sampling
        val top_k: Int = 50,                   // Added top-k for better quality
        val repetition_penalty: Float = 1.2f,  // Prevent repetition
        val return_full_text: Boolean = false,
        val do_sample: Boolean = true,
        val pad_token_id: Int = 50256,
        // Add stop sequences to prevent overly long responses
        val stop_sequence: String? = "\n\n"
    )
}

/**
 * Response model from Hugging Face API
 */
data class HuggingFaceResponse(
    val generated_text: String? = null,
    val error: String? = null
)
