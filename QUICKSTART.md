# Quick Start Guide

Get your AI Assistant running in 5 minutes!

## Step 1: Get Hugging Face API Key (2 minutes)

1. Go to [Hugging Face](https://huggingface.co/)
2. Click "Sign Up" (or "Log In" if you have an account)
3. After signing in, go to Settings → Access Tokens
4. Click "New token"
5. Give it a name (e.g., "AI Assistant App")
6. Select "Read" permission
7. Click "Generate"
8. **Copy the token** - you'll need it in the app!

## Step 2: Build the App (2 minutes)

### Option A: Using Android Studio (Recommended)

1. Open Android Studio
2. Click "Open" and select this project folder
3. Wait for Gradle sync (downloads dependencies automatically)
4. Click the green "Run" button (or press Shift+F10)
5. Select your device/emulator
6. Wait for the app to install and launch

### Option B: Using Command Line

```bash
# Linux/Mac
./gradlew assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk

# Windows
gradlew.bat assembleDebug
adb install app\build\outputs\apk\debug\app-debug.apk
```

## Step 3: Configure API Key (1 minute)

1. App opens to the chat screen
2. Tap the ⚙️ (Settings) icon in the top-right corner
3. Paste your Hugging Face API key in the "API Key" field
4. Tap "Save API Key"
5. Tap the back arrow to return to chat

## Step 4: Start Chatting! (30 seconds)

1. Type your first message in the text field at the bottom
2. Tap the send button (➤)
3. Watch the AI respond!
4. Continue the conversation naturally

## Example First Messages

Try these to get started:

- "Hello! What can you help me with?"
- "Explain quantum computing in simple terms"
- "Write a haiku about coding"
- "What are the best practices for Android development?"
- "Tell me a joke"

## Troubleshooting

### "Please configure your Hugging Face API key first"
→ You haven't set up your API key yet. Go to Settings (⚙️) and add it.

### "Failed to get response"
→ Check your internet connection and ensure your API key is correct.

### App won't build
→ Make sure you have:
  - Android Studio Hedgehog or later
  - Internet connection (for downloading dependencies)
  - Android SDK API 24 or higher installed

### Gradle sync failed
→ File → Invalidate Caches / Restart in Android Studio

## Tips for Best Results

1. **Be Specific**: The more detailed your question, the better the response
2. **Context Matters**: The AI remembers the conversation context
3. **Be Patient**: First response might take a few seconds (model loading)
4. **Experiment**: Try different types of questions and prompts
5. **Clear Chat**: Use Settings → Clear Chat to start fresh conversations

## Key Features to Explore

- **Message History**: Scroll through past messages
- **Error Messages**: Watch for error notifications at the top
- **Settings**: Customize your API key and manage chat
- **Auto-scroll**: New messages automatically scroll into view
- **Loading Indicator**: See when the AI is thinking

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- See [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
- Review [BUILD.md](BUILD.md) for advanced build options
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute improvements

## What's Next?

Now that you're up and running:

1. Have a conversation with the AI
2. Try different types of questions
3. Explore the Settings screen
4. Read the architecture documentation
5. Consider contributing improvements!

## Security Reminder

⚠️ **Keep your API key private!**
- Don't share screenshots with the key visible
- Don't commit it to version control
- Don't share the key with others

---

**Enjoy your AI Assistant! 🤖✨**
