# AI Assistant Android App

An Android AI assistant chat application featuring the latest Android development technologies and powered by Hugging Face API.

## Features

- 🤖 **AI-Powered Chat**: Utilizes Hugging Face's Mistral-7B-Instruct-v0.2 model for intelligent conversations
- 💬 **Modern UI**: Built with Jetpack Compose and Material 3 design
- 🎨 **Dynamic Theming**: Supports Material You dynamic colors (Android 12+)
- 🔐 **Secure API Key Storage**: Configurable API key management
- 📱 **Responsive Design**: Optimized for various screen sizes
- ⚡ **Real-time Chat**: Async message processing with loading states
- 🎯 **Clean Architecture**: MVVM pattern with Repository and ViewModel layers

## Technologies Used

### Build System
- **Gradle 8.11.1**: Modern build automation
- **AGP 8.7.3**: Android Gradle Plugin
- **Version Catalog**: Centralized dependency management via `libs.versions.toml`

### Core Technologies
- **Kotlin 2.1.0**: Modern programming language for Android
- **Jetpack Compose**: Declarative UI toolkit
- **Material 3**: Latest Material Design components
- **Coroutines 1.9.0**: Asynchronous programming

### Architecture Components
- **ViewModel**: Lifecycle-aware UI data management
- **StateFlow**: Reactive state management
- **Repository Pattern**: Data layer abstraction

### Networking
- **Retrofit 2.11.0**: Type-safe HTTP client
- **OkHttp 4.12.0**: HTTP client with logging interceptor
- **Gson**: JSON serialization/deserialization

### AI Integration
- **Hugging Face API**: Access to state-of-the-art language models
- **Mistral-7B-Instruct-v0.2**: Default AI model for chat interactions

## Project Structure

```
app/
├── src/main/
│   ├── java/com/aiassistant/chat/
│   │   ├── api/
│   │   │   ├── HuggingFaceApiService.kt    # Retrofit API interface
│   │   │   └── RetrofitClient.kt           # Retrofit configuration
│   │   ├── model/
│   │   │   ├── ChatMessage.kt              # Chat message data model
│   │   │   └── HuggingFaceModels.kt        # API request/response models
│   │   ├── repository/
│   │   │   └── ChatRepository.kt           # Data repository
│   │   ├── viewmodel/
│   │   │   └── ChatViewModel.kt            # UI state management
│   │   ├── ui/
│   │   │   ├── ChatScreen.kt               # Main chat interface
│   │   │   ├── MessageItem.kt              # Individual message UI
│   │   │   ├── SettingsScreen.kt           # Settings interface
│   │   │   └── theme/                      # App theming
│   │   └── MainActivity.kt                 # App entry point
│   ├── res/                                 # Resources
│   └── AndroidManifest.xml                 # App manifest
└── build.gradle.kts                        # App-level build config
```

## Setup Instructions

### Prerequisites
- Android Studio Hedgehog or later
- JDK 8 or later
- Android SDK (API 24+)
- Hugging Face API key

### Getting Your Hugging Face API Key
1. Visit [Hugging Face](https://huggingface.co/)
2. Create an account or sign in
3. Go to Settings → Access Tokens
4. Create a new token with read permissions
5. Copy your API key

### Building the App

1. **Clone the repository**:
   ```bash
   git clone https://github.com/patricklarocque1/AI-assistant-android.git
   cd AI-assistant-android
   ```

2. **Open in Android Studio**:
   - Launch Android Studio
   - Select "Open an Existing Project"
   - Navigate to the cloned repository

3. **Sync Gradle**:
   - Android Studio will automatically sync Gradle
   - Wait for dependencies to download

4. **Run the app**:
   - Connect an Android device or start an emulator
   - Click the "Run" button or press Shift+F10

### Configuration

On first launch:
1. Tap the Settings icon (⚙️) in the top right
2. Enter your Hugging Face API key
3. Tap "Save API Key"
4. Return to the chat screen and start chatting!

## Usage

### Chatting with the AI
- Type your message in the input field at the bottom
- Press the send button (➤) or Enter
- Wait for the AI to respond
- The AI will provide intelligent responses based on your input

### Settings
- **API Key**: Configure your Hugging Face API key
- **Clear Chat**: Delete all conversation history
- **Model Info**: View current AI model information

## API Integration

The app integrates with Hugging Face's Inference API:

### Endpoint
```
POST https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2
```

### Request Format
```json
{
  "inputs": "Your message here",
  "parameters": {
    "max_new_tokens": 250,
    "temperature": 0.7,
    "top_p": 0.95,
    "return_full_text": false
  }
}
```

### Headers
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## Customization

### Changing the AI Model
Edit `HuggingFaceApiService.kt`:
```kotlin
@POST("models/YOUR_MODEL_HERE")
suspend fun query(...)
```

### Adjusting Generation Parameters
Edit `HuggingFaceModels.kt`:
```kotlin
data class Parameters(
    val max_new_tokens: Int = 250,      // Max response length
    val temperature: Float = 0.7f,       // Randomness (0-1)
    val top_p: Float = 0.95f,           // Nucleus sampling
    val return_full_text: Boolean = false
)
```

### UI Customization
- Modify colors in `Color.kt`
- Adjust typography in `Type.kt`
- Change theme in `Theme.kt`

## Requirements

- **Minimum SDK**: API 24 (Android 7.0)
- **Target SDK**: API 34 (Android 14)
- **Internet Permission**: Required for API calls

## Dependencies

Key dependencies (see `app/build.gradle.kts` for complete list):
- androidx.compose.bom:2023.10.01
- androidx.lifecycle:lifecycle-viewmodel-compose:2.6.2
- com.squareup.retrofit2:retrofit:2.9.0
- com.squareup.okhttp3:okhttp:4.12.0
- org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3

## Troubleshooting

### Build Issues
- Ensure Gradle is synced
- Clean and rebuild: Build → Clean Project, then Build → Rebuild Project
- Invalidate caches: File → Invalidate Caches / Restart

### Network Errors
- Check internet connection
- Verify API key is correct
- Ensure Hugging Face API is accessible

### API Errors
- "Model is loading": Wait a few seconds and try again
- "Unauthorized": Check your API key
- "Rate limit": Wait before making more requests

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [Jetpack Compose](https://developer.android.com/jetpack/compose)
- Powered by [Hugging Face](https://huggingface.co/)
- Uses [Mistral AI](https://mistral.ai/) models

## Contact

For questions or feedback, please open an issue on GitHub.
