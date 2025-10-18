package com.aiassistant.chat.model

/**
 * Configuration for AI text generation parameters
 */
data class GenerationConfig(
    val maxLength: Int = 64, // Default for short responses
    val temperature: Float = 0.7f,
    val topP: Float = 0.9f
)
