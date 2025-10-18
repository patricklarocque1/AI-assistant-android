package com.aiassistant.chat.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.aiassistant.chat.viewmodel.ServerConfigViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ServerConfigScreen(
    onBack: () -> Unit,
    viewModel: ServerConfigViewModel = viewModel()
) {
    val config by viewModel.config.collectAsState()
    val systemInfo by viewModel.systemInfo.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val errorMessage by viewModel.errorMessage.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Server Configuration") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { viewModel.refreshConfig() }) {
                        Icon(Icons.Default.Refresh, "Refresh")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Error message
            errorMessage?.let { error ->
                Card(
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer
                    )
                ) {
                    Text(
                        text = error,
                        modifier = Modifier.padding(16.dp),
                        color = MaterialTheme.colorScheme.onErrorContainer
                    )
                }
            }

            // Loading indicator
            if (isLoading) {
                LinearProgressIndicator(
                    modifier = Modifier.fillMaxWidth()
                )
            }

            // System Information Card
            systemInfo?.let { info ->
                SystemInfoCard(info)
            }

            // Model Configuration Card
            config?.let { cfg ->
                ModelConfigCard(
                    config = cfg,
                    onModelChange = { viewModel.updateModel(it) },
                    onCacheDirChange = { viewModel.updateCacheDir(it) }
                )
            }

            // Performance Settings Card
            config?.let { cfg ->
                PerformanceSettingsCard(
                    config = cfg,
                    onGpuToggle = { viewModel.updateGpuUsage(it) },
                    on8BitToggle = { viewModel.update8Bit(it) },
                    on4BitToggle = { viewModel.update4Bit(it) }
                )
            }

            // Generation Settings Card
            config?.let { cfg ->
                GenerationSettingsCard(
                    config = cfg,
                    onMaxLengthChange = { viewModel.updateMaxLength(it) },
                    onTemperatureChange = { viewModel.updateTemperature(it) },
                    onTopPChange = { viewModel.updateTopP(it) }
                )
            }

            // Action Buttons
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedButton(
                    onClick = { viewModel.saveConfiguration() },
                    modifier = Modifier.weight(1f),
                    enabled = !isLoading
                ) {
                    Icon(Icons.Default.Save, null)
                    Spacer(Modifier.width(8.dp))
                    Text("Save Config")
                }

                Button(
                    onClick = { viewModel.restartServer() },
                    modifier = Modifier.weight(1f),
                    enabled = !isLoading
                ) {
                    Icon(Icons.Default.Refresh, null)
                    Spacer(Modifier.width(8.dp))
                    Text("Restart Server")
                }
            }

            // Info text
            Text(
                text = "Note: Configuration changes require a server restart to take effect.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun SystemInfoCard(info: Map<String, Any>) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "System Information",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )

            Divider()

            InfoRow("Device", info["device"] as? String ?: "Unknown")
            InfoRow("Model Loaded", if (info["model_loaded"] as? Boolean == true) "Yes" else "No")
            
            val uptimeSeconds = (info["uptime_seconds"] as? Number)?.toLong() ?: 0
            val uptimeFormatted = formatUptime(uptimeSeconds)
            InfoRow("Uptime", uptimeFormatted)

            val cpuPercent = (info["cpu_percent"] as? Number)?.toFloat() ?: 0f
            InfoRow("CPU Usage", String.format("%.1f%%", cpuPercent))

            val memoryPercent = (info["memory_percent"] as? Number)?.toFloat() ?: 0f
            val memoryUsed = (info["memory_used_gb"] as? Number)?.toFloat() ?: 0f
            val memoryTotal = (info["memory_total_gb"] as? Number)?.toFloat() ?: 0f
            InfoRow("Memory", String.format("%.1f / %.1f GB (%.1f%%)", 
                memoryUsed, memoryTotal, memoryPercent))

            if (info["gpu_memory_used_gb"] != null) {
                val gpuUsed = (info["gpu_memory_used_gb"] as? Number)?.toFloat() ?: 0f
                val gpuTotal = (info["gpu_memory_total_gb"] as? Number)?.toFloat() ?: 0f
                InfoRow("GPU Memory", String.format("%.1f / %.1f GB", gpuUsed, gpuTotal))
            }
        }
    }
}

@Composable
fun ModelConfigCard(
    config: Map<String, Any>,
    onModelChange: (String) -> Unit,
    onCacheDirChange: (String) -> Unit
) {
    var showModelDialog by remember { mutableStateOf(false) }
    var showCacheDirDialog by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Model Configuration",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )

            Divider()

            InfoRow("Model Name", config["model_name"] as? String ?: "Unknown")
            TextButton(onClick = { showModelDialog = true }) {
                Text("Change Model")
            }

            InfoRow("Cache Directory", config["model_cache_dir"] as? String ?: "Default")
            TextButton(onClick = { showCacheDirDialog = true }) {
                Text("Change Cache Dir")
            }

            InfoRow("HuggingFace Token", if (config["has_hf_token"] as? Boolean == true) "Configured" else "Not set")
        }
    }

    if (showModelDialog) {
        ModelSelectionDialog(
            currentModel = config["model_name"] as? String ?: "",
            onDismiss = { showModelDialog = false },
            onConfirm = { newModel ->
                onModelChange(newModel)
                showModelDialog = false
            }
        )
    }

    if (showCacheDirDialog) {
        CacheDirDialog(
            currentDir = config["model_cache_dir"] as? String ?: "",
            onDismiss = { showCacheDirDialog = false },
            onConfirm = { newDir ->
                onCacheDirChange(newDir)
                showCacheDirDialog = false
            }
        )
    }
}

@Composable
fun PerformanceSettingsCard(
    config: Map<String, Any>,
    onGpuToggle: (Boolean) -> Unit,
    on8BitToggle: (Boolean) -> Unit,
    on4BitToggle: (Boolean) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Performance Settings",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )

            Divider()

            val cudaAvailable = config["cuda_available"] as? Boolean == true
            val gpuName = config["gpu_name"] as? String

            if (cudaAvailable && gpuName != null) {
                InfoRow("GPU Detected", gpuName)
            } else {
                InfoRow("GPU", "Not available")
            }

            SwitchRow(
                label = "Use GPU",
                checked = config["use_gpu"] as? Boolean == true,
                onCheckedChange = onGpuToggle,
                enabled = cudaAvailable
            )

            SwitchRow(
                label = "8-bit Quantization (50% memory)",
                checked = config["load_in_8bit"] as? Boolean == true,
                onCheckedChange = on8BitToggle
            )

            SwitchRow(
                label = "4-bit Quantization (75% memory)",
                checked = config["load_in_4bit"] as? Boolean == true,
                onCheckedChange = on4BitToggle
            )
        }
    }
}

@Composable
fun GenerationSettingsCard(
    config: Map<String, Any>,
    onMaxLengthChange: (Int) -> Unit,
    onTemperatureChange: (Float) -> Unit,
    onTopPChange: (Float) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Generation Settings",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )

            Divider()

            val maxLength = (config["default_max_length"] as? Number)?.toInt() ?: 100
            SliderRow(
                label = "Max Length",
                value = maxLength.toFloat(),
                valueRange = 10f..500f,
                steps = 49,
                onValueChange = { onMaxLengthChange(it.toInt()) },
                valueText = maxLength.toString()
            )

            val temperature = (config["default_temperature"] as? Number)?.toFloat() ?: 0.8f
            SliderRow(
                label = "Temperature",
                value = temperature,
                valueRange = 0.1f..2.0f,
                steps = 19,
                onValueChange = onTemperatureChange,
                valueText = String.format("%.2f", temperature)
            )

            val topP = (config["default_top_p"] as? Number)?.toFloat() ?: 0.9f
            SliderRow(
                label = "Top P",
                value = topP,
                valueRange = 0.1f..1.0f,
                steps = 9,
                onValueChange = onTopPChange,
                valueText = String.format("%.2f", topP)
            )
        }
    }
}

@Composable
fun InfoRow(label: String, value: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium
        )
    }
}

@Composable
fun SwitchRow(
    label: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    enabled: Boolean = true
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium
        )
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            enabled = enabled
        )
    }
}

@Composable
fun SliderRow(
    label: String,
    value: Float,
    valueRange: ClosedFloatingPointRange<Float>,
    steps: Int,
    onValueChange: (Float) -> Unit,
    valueText: String
) {
    Column {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.bodyMedium
            )
            Text(
                text = valueText,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
        }
        Slider(
            value = value,
            onValueChange = onValueChange,
            valueRange = valueRange,
            steps = steps
        )
    }
}

@Composable
fun ModelSelectionDialog(
    currentModel: String,
    onDismiss: () -> Unit,
    onConfirm: (String) -> Unit
) {
    var selectedModel by remember { mutableStateOf(currentModel) }

    val popularModels = listOf(
        "Qwen/Qwen3-0.6B" to "Qwen 0.6B (Fast, lightweight)",
        "meta-llama/Llama-3.2-1B-Instruct" to "Llama 3.2 1B (Better quality)",
        "microsoft/DialoGPT-medium" to "DialoGPT Medium (Conversational)",
        "Gensyn/Qwen2.5-0.5B-Instruct" to "Qwen 2.5 0.5B (Very fast)",
        "Custom" to "Enter custom model name"
    )

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Select AI Model") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                popularModels.forEach { (model, description) ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        RadioButton(
                            selected = selectedModel == model || (model == "Custom" && !popularModels.any { it.first == selectedModel }),
                            onClick = { selectedModel = model }
                        )
                        Column {
                            Text(model, style = MaterialTheme.typography.bodyMedium)
                            Text(description, style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }

                if (!popularModels.any { it.first == selectedModel }) {
                    OutlinedTextField(
                        value = selectedModel,
                        onValueChange = { selectedModel = it },
                        label = { Text("Custom Model") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            }
        },
        confirmButton = {
            Button(onClick = { onConfirm(selectedModel) }) {
                Text("Apply")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
fun CacheDirDialog(
    currentDir: String,
    onDismiss: () -> Unit,
    onConfirm: (String) -> Unit
) {
    var directory by remember { mutableStateOf(currentDir) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Model Cache Directory") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Enter the path where models should be stored on your Ubuntu PC:")
                OutlinedTextField(
                    value = directory,
                    onValueChange = { directory = it },
                    label = { Text("Directory Path") },
                    placeholder = { Text("/home/username/ai-models") },
                    modifier = Modifier.fillMaxWidth()
                )
                Text(
                    "Examples:\n• /home/username/ai-models\n• /mnt/ssd/models\n• ~/Desktop/AI-Models",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        },
        confirmButton = {
            Button(onClick = { onConfirm(directory) }) {
                Text("Apply")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

fun formatUptime(seconds: Long): String {
    val days = seconds / 86400
    val hours = (seconds % 86400) / 3600
    val minutes = (seconds % 3600) / 60
    val secs = seconds % 60

    return when {
        days > 0 -> "${days}d ${hours}h ${minutes}m"
        hours > 0 -> "${hours}h ${minutes}m ${secs}s"
        minutes > 0 -> "${minutes}m ${secs}s"
        else -> "${secs}s"
    }
}
