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

enum class Screen {
    CHAT, SETTINGS, SERVER_CONFIG
}

@Composable
fun AIAssistantApp() {
    val viewModel: ChatViewModel = viewModel()
    var currentScreen by remember { mutableStateOf(Screen.CHAT) }
    
    when (currentScreen) {
        Screen.CHAT -> {
            ChatScreen(
                viewModel = viewModel,
                onSettingsClick = { currentScreen = Screen.SETTINGS }
            )
        }
        Screen.SETTINGS -> {
            SettingsScreen(
                viewModel = viewModel,
                onBackClick = { currentScreen = Screen.CHAT },
                onServerConfigClick = { currentScreen = Screen.SERVER_CONFIG }
            )
        }
        Screen.SERVER_CONFIG -> {
            com.aiassistant.chat.ui.ServerConfigScreen(
                onBack = { currentScreen = Screen.SETTINGS }
            )
        }
    }
}
