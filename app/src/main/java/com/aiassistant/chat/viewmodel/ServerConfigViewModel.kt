package com.aiassistant.chat.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aiassistant.chat.repository.ServerConfigRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ServerConfigViewModel : ViewModel() {
    private val repository = ServerConfigRepository()

    private val _config = MutableStateFlow<Map<String, Any>?>(null)
    val config: StateFlow<Map<String, Any>?> = _config

    private val _systemInfo = MutableStateFlow<Map<String, Any>?>(null)
    val systemInfo: StateFlow<Map<String, Any>?> = _systemInfo

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage

    private val pendingUpdates = mutableMapOf<String, Any>()

    init {
        refreshConfig()
    }

    fun refreshConfig() {
        viewModelScope.launch {
            _isLoading.value = true
            _errorMessage.value = null

            try {
                // Fetch config
                val configResult = repository.getConfig()
                if (configResult.isSuccess) {
                    _config.value = configResult.getOrNull()
                } else {
                    _errorMessage.value = "Failed to load configuration: ${configResult.exceptionOrNull()?.message}"
                }

                // Fetch system info
                val systemResult = repository.getSystemInfo()
                if (systemResult.isSuccess) {
                    _systemInfo.value = systemResult.getOrNull()
                }

            } catch (e: Exception) {
                _errorMessage.value = "Error: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun updateModel(modelName: String) {
        pendingUpdates["model_name"] = modelName
        updateLocalConfig("model_name", modelName)
    }

    fun updateCacheDir(cacheDir: String) {
        pendingUpdates["model_cache_dir"] = cacheDir
        updateLocalConfig("model_cache_dir", cacheDir)
    }

    fun updateGpuUsage(enabled: Boolean) {
        pendingUpdates["use_gpu"] = enabled
        updateLocalConfig("use_gpu", enabled)
    }

    fun update8Bit(enabled: Boolean) {
        pendingUpdates["load_in_8bit"] = enabled
        updateLocalConfig("load_in_8bit", enabled)
        // Disable 4-bit if 8-bit is enabled
        if (enabled) {
            pendingUpdates["load_in_4bit"] = false
            updateLocalConfig("load_in_4bit", false)
        }
    }

    fun update4Bit(enabled: Boolean) {
        pendingUpdates["load_in_4bit"] = enabled
        updateLocalConfig("load_in_4bit", enabled)
        // Disable 8-bit if 4-bit is enabled
        if (enabled) {
            pendingUpdates["load_in_8bit"] = false
            updateLocalConfig("load_in_8bit", false)
        }
    }

    fun updateMaxLength(length: Int) {
        pendingUpdates["default_max_length"] = length
        updateLocalConfig("default_max_length", length)
    }

    fun updateTemperature(temp: Float) {
        pendingUpdates["default_temperature"] = temp
        updateLocalConfig("default_temperature", temp)
    }

    fun updateTopP(topP: Float) {
        pendingUpdates["default_top_p"] = topP
        updateLocalConfig("default_top_p", topP)
    }

    private fun updateLocalConfig(key: String, value: Any) {
        _config.value = _config.value?.toMutableMap()?.apply {
            put(key, value)
        }
    }

    fun saveConfiguration() {
        if (pendingUpdates.isEmpty()) {
            _errorMessage.value = "No changes to save"
            return
        }

        viewModelScope.launch {
            _isLoading.value = true
            _errorMessage.value = null

            try {
                val result = repository.updateConfig(pendingUpdates)
                if (result.isSuccess) {
                    pendingUpdates.clear()
                    _errorMessage.value = "Configuration saved! Restart server to apply changes."
                    refreshConfig()
                } else {
                    _errorMessage.value = "Failed to save: ${result.exceptionOrNull()?.message}"
                }
            } catch (e: Exception) {
                _errorMessage.value = "Error saving: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun restartServer() {
        viewModelScope.launch {
            _isLoading.value = true
            _errorMessage.value = null

            try {
                val result = repository.restartServer()
                if (result.isSuccess) {
                    _errorMessage.value = "Restart signal sent! Server will restart shortly."
                } else {
                    _errorMessage.value = "Failed to restart: ${result.exceptionOrNull()?.message}"
                }
            } catch (e: Exception) {
                _errorMessage.value = "Error restarting: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }
}
