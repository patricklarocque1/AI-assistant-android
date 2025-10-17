package com.aiassistant.chat.api

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Retrofit client for local AI server
 */
object LocalRetrofitClient {
    
    private var currentBaseUrl: String = ""
    private var retrofit: Retrofit? = null
    
    /**
     * Initialize or update the Retrofit client with a new base URL
     * @param baseUrl The base URL of your local server (Ngrok URL)
     */
    fun initialize(baseUrl: String) {
        if (baseUrl.isEmpty()) {
            throw IllegalArgumentException("Base URL cannot be empty")
        }
        
        // Ensure URL ends with /
        currentBaseUrl = if (baseUrl.endsWith("/")) baseUrl else "$baseUrl/"
        
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        
        val client = OkHttpClient.Builder()
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)  // AI generation can take time
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
        
        retrofit = Retrofit.Builder()
            .baseUrl(currentBaseUrl)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
    
    /**
     * Get the LocalAiApiService instance
     * @throws IllegalStateException if client hasn't been initialized
     */
    fun getApiService(): LocalAiApiService {
        if (retrofit == null) {
            throw IllegalStateException(
                "LocalRetrofitClient must be initialized with a base URL first. " +
                "Call LocalRetrofitClient.initialize(baseUrl) before using the API."
            )
        }
        return retrofit!!.create(LocalAiApiService::class.java)
    }
    
    /**
     * Check if client is initialized
     */
    fun isInitialized(): Boolean {
        return retrofit != null
    }
    
    /**
     * Get current base URL
     */
    fun getCurrentBaseUrl(): String {
        return currentBaseUrl
    }
}
