package com.aiassistant.chat.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.aiassistant.chat.viewmodel.ChatViewModel

/**
 * Settings screen composable
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    viewModel: ChatViewModel,
    onBackClick: () -> Unit,
    onServerConfigClick: () -> Unit = {}
) {
    val apiKey by viewModel.apiKey.collectAsState()
    val useLocalServer by viewModel.useLocalServer.collectAsState()
    val localServerUrl by viewModel.localServerUrl.collectAsState()
    val serverStatus by viewModel.serverStatus.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    
    var apiKeyInput by remember { mutableStateOf(apiKey ?: "") }
    var localServerUrlInput by remember { mutableStateOf(localServerUrl) }
    var showClearDialog by remember { mutableStateOf(false) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            // Server Selection
            Text(
                text = "AI Server Configuration",
                style = MaterialTheme.typography.titleLarge,
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Server Type Switch
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                )
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "Use Local Server",
                            style = MaterialTheme.typography.titleMedium
                        )
                        Text(
                            text = if (useLocalServer) "Using your local AI model" else "Using Hugging Face API",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    Switch(
                        checked = useLocalServer,
                        onCheckedChange = { 
                            viewModel.setUseLocalServer(it)
                        }
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Show appropriate configuration based on server type
            if (useLocalServer) {
                // Local Server Configuration
                Text(
                    text = "Local Server Settings",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary
                )
                
                Spacer(modifier = Modifier.height(12.dp))
                
                OutlinedTextField(
                    value = localServerUrlInput,
                    onValueChange = { localServerUrlInput = it },
                    label = { Text("Server URL") },
                    placeholder = { Text("https://your-ngrok-url.ngrok-free.dev") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Uri)
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(
                    text = "Enter your Ngrok URL from the local server",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Spacer(modifier = Modifier.height(12.dp))
                
                // Server status
                if (serverStatus != null) {
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(
                            containerColor = if (serverStatus!!.contains("✅")) 
                                MaterialTheme.colorScheme.primaryContainer
                            else 
                                MaterialTheme.colorScheme.errorContainer
                        )
                    ) {
                        Text(
                            text = serverStatus!!,
                            modifier = Modifier.padding(12.dp),
                            style = MaterialTheme.typography.bodyMedium
                        )
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                }
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            viewModel.setLocalServerUrl(localServerUrlInput)
                            viewModel.testLocalServerConnection()
                        },
                        modifier = Modifier.weight(1f),
                        enabled = !isLoading && localServerUrlInput.isNotBlank()
                    ) {
                        Text("Test Connection")
                    }
                    
                    Button(
                        onClick = {
                            viewModel.setLocalServerUrl(localServerUrlInput)
                            onBackClick()
                        },
                        modifier = Modifier.weight(1f),
                        enabled = localServerUrlInput.isNotBlank()
                    ) {
                        Text("Save")
                    }
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                
                // Server Configuration Button
                OutlinedButton(
                    onClick = onServerConfigClick,
                    modifier = Modifier.fillMaxWidth(),
                    enabled = localServerUrlInput.isNotBlank()
                ) {
                    Text("Manage Server Configuration")
                }
            } else {
                // Hugging Face Configuration
                Text(
                    text = "Hugging Face Configuration",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary
                )
                
                Spacer(modifier = Modifier.height(12.dp))
                
                OutlinedTextField(
                    value = apiKeyInput,
                    onValueChange = { apiKeyInput = it },
                    label = { Text("API Key") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    visualTransformation = PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(
                    text = "Get your API key from huggingface.co",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Button(
                    onClick = {
                        viewModel.setApiKey(apiKeyInput)
                        onBackClick()
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Save API Key")
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Divider()
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Text(
                text = "Chat Management",
                style = MaterialTheme.typography.titleLarge,
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedButton(
                onClick = { showClearDialog = true },
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(
                    Icons.Default.Delete,
                    contentDescription = "Clear Chat",
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("Clear Chat History")
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Text(
                text = "Model Information",
                style = MaterialTheme.typography.titleLarge,
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                )
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "Current Model",
                        style = MaterialTheme.typography.titleMedium
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = if (useLocalServer) {
                            "Local: GPT-2 (or configured model)"
                        } else {
                            "Hugging Face: mistralai/Mistral-7B-Instruct-v0.2"
                        },
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    
                    if (useLocalServer) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "💡 Running on your PC",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }
        }
    }
    
    if (showClearDialog) {
        AlertDialog(
            onDismissRequest = { showClearDialog = false },
            title = { Text("Clear Chat History") },
            text = { Text("Are you sure you want to clear all messages? This action cannot be undone.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.clearMessages()
                        showClearDialog = false
                        onBackClick()
                    }
                ) {
                    Text("Clear")
                }
            },
            dismissButton = {
                TextButton(onClick = { showClearDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
}
