package com.aiassistant.chat.model

import java.util.UUID

/**
 * Represents a chat message in the conversation
 */
data class ChatMessage(
    val id: String = UUID.randomUUID().toString(),
    val content: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis()
)
