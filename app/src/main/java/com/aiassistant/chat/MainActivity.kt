package com.aiassistant.chat

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import com.aiassistant.chat.ui.ChatScreen
import com.aiassistant.chat.ui.SettingsScreen
import com.aiassistant.chat.ui.theme.AIAssistantTheme
import com.aiassistant.chat.viewmodel.ChatViewModel

/**
 * Main Activity for the AI Assistant Chat application
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AIAssistantTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AIAssistantApp()
                }
            }
        }
    }
}

@Composable
fun AIAssistantApp() {
    val viewModel: ChatViewModel = viewModel()
    var showSettings by remember { mutableStateOf(false) }
    
    if (showSettings) {
        SettingsScreen(
            viewModel = viewModel,
            onBackClick = { showSettings = false }
        )
    } else {
        ChatScreen(
            viewModel = viewModel,
            onSettingsClick = { showSettings = true }
        )
    }
}
