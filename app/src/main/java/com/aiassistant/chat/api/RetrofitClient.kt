package com.aiassistant.chat.api

import okhttp3.Cache
import okhttp3.ConnectionPool
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.File
import java.util.concurrent.TimeUnit

/**
 * Singleton object to create and provide Retrofit instance
 * Optimized for efficient API communication
 */
object RetrofitClient {
    
    private const val BASE_URL = "https://api-inference.huggingface.co/"
    private const val CACHE_SIZE = 10L * 1024 * 1024 // 10 MB cache
    
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        // Use BASIC level in production for better performance
        level = HttpLoggingInterceptor.Level.BASIC
    }
    
    // Connection pooling for faster subsequent requests
    private val connectionPool = ConnectionPool(
        maxIdleConnections = 5,
        keepAliveDuration = 5,
        timeUnit = TimeUnit.MINUTES
    )
    
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        // Optimized timeouts for better responsiveness
        .connectTimeout(15, TimeUnit.SECONDS)  // Reduced from 30s
        .readTimeout(45, TimeUnit.SECONDS)     // Increased for model generation
        .writeTimeout(15, TimeUnit.SECONDS)    // Reduced from 30s
        .connectionPool(connectionPool)
        // Enable HTTP/2 for better performance
        .retryOnConnectionFailure(true)
        .build()
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val apiService: HuggingFaceApiService by lazy {
        retrofit.create(HuggingFaceApiService::class.java)
    }
}
