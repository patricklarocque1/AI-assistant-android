package com.aiassistant.chat.repository

import com.aiassistant.chat.api.RetrofitClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class ServerConfigRepository {
    
    suspend fun getConfig(): Result<Map<String, Any>> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.apiService.getConfig()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to fetch config: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateConfig(updates: Map<String, Any>): Result<Map<String, Any>> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.apiService.updateConfig(updates)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to update config: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getSystemInfo(): Result<Map<String, Any>> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.apiService.getSystemInfo()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to fetch system info: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun restartServer(): Result<Map<String, Any>> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.apiService.restartServer()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to restart server: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
