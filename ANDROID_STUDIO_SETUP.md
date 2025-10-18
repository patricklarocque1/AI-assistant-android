# Android Studio Setup Guide

This guide will help you set up the AI Assistant project in Android Studio and configure the Hugging Face API connection.

## Prerequisites

- **Android Studio** Hedgehog (2023.1.1) or later
- **JDK 17** or later
- **Android SDK** with API level 24-34
- **Hugging Face Account** with API token

## Step 1: Install Android Studio

1. Download Android Studio from [developer.android.com](https://developer.android.com/studio)
2. Install following the instructions for your OS
3. Open Android Studio and complete the setup wizard
4. Install the Android SDK (if not already installed)

## Step 2: Open the Project

1. Launch Android Studio
2. Click **"Open"** (or File → Open)
3. Navigate to the project directory
4. Select the root folder containing `build.gradle.kts`
5. Click **"OK"**

## Step 3: Gradle Sync

Android Studio will automatically start syncing Gradle. If not:

1. Click **"Sync Now"** in the notification bar
2. Or go to **File → Sync Project with Gradle Files**
3. Wait for the sync to complete (first time may take 5-10 minutes)

### Common Gradle Sync Issues

#### Issue: "Gradle version X is required"
**Solution**: The project uses Gradle 8.2 and AGP 8.1.4. Update your Android Studio to the latest version.

#### Issue: "SDK location not found"
**Solution**: 
1. Go to **File → Project Structure → SDK Location**
2. Set the Android SDK location (usually `~/Android/Sdk` on Mac/Linux or `C:\Users\YourName\AppData\Local\Android\Sdk` on Windows)

#### Issue: "Build Tools not found"
**Solution**: 
1. Go to **Tools → SDK Manager**
2. Install **Android SDK Build-Tools 33.0.1** or later
3. Click **Apply** and wait for installation

## Step 4: Configure SDK

1. Open **Tools → SDK Manager**
2. In **SDK Platforms** tab, install:
   - Android 14.0 (API 34) - Target SDK
   - Android 7.0 (API 24) - Minimum SDK
3. In **SDK Tools** tab, ensure these are installed:
   - Android SDK Build-Tools 33.0.1+
   - Android SDK Platform-Tools
   - Android SDK Tools
   - Android Emulator (if testing on emulator)

## Step 5: Build the Project

### Option 1: Using Android Studio UI
1. Click **Build → Make Project** (or Ctrl+F9 / Cmd+F9)
2. Wait for the build to complete
3. Check the **Build** panel for any errors

### Option 2: Using Terminal
```bash
# In Android Studio's Terminal panel (Alt+F12)
./gradlew assembleDebug
```

### Verify Build Success
After successful build, you should see:
- **"BUILD SUCCESSFUL"** message
- APK at: `app/build/outputs/apk/debug/app-debug.apk`
- No errors in the Build panel

## Step 6: Run the Application

### On Physical Device
1. Enable **Developer Options** on your Android device:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
2. Enable **USB Debugging** in Developer Options
3. Connect device via USB
4. Click the **Run** button (green play icon) or press Shift+F10
5. Select your device from the list

### On Emulator
1. Click **Device Manager** in the toolbar
2. Click **Create Device**
3. Select a device (e.g., Pixel 5)
4. Select a system image (API 34 recommended)
5. Click **Finish**
6. Click **Run** and select the emulator

## Step 7: Configure Hugging Face API

### Get Your API Token

1. Go to [huggingface.co](https://huggingface.co/)
2. Sign in or create an account
3. Go to **Settings → Access Tokens**
4. Click **"New token"**
5. Enter a name (e.g., "AI Assistant App")
6. Select **"Read"** permission
7. Click **"Generate token"**
8. **Copy the token** (you won't see it again!)

### Add Token to the App

1. Run the app on your device/emulator
2. You'll see the chat screen
3. Tap the **Settings icon (⚙️)** in the top-right
4. Paste your Hugging Face API token in the **"API Key"** field
5. Tap **"Save API Key"**
6. Go back to the chat screen

### Test the Connection

1. Type a test message: `"Hello, can you help me?"`
2. Tap **Send (➤)**
3. You should see:
   - A loading indicator
   - AI response appears in a gray bubble
4. If you see an error:
   - Check your internet connection
   - Verify the API token is correct
   - See troubleshooting section below

## Troubleshooting

### Build Issues

#### Error: "Unsupported class file major version"
**Cause**: JDK version mismatch  
**Solution**: 
1. Go to **File → Project Structure → SDK Location**
2. Set JDK to version 17
3. Download JDK 17 if needed from [adoptium.net](https://adoptium.net/)

#### Error: "Could not resolve dependencies"
**Cause**: Network issues or repository problems  
**Solution**:
```bash
# Clear Gradle cache
./gradlew clean --refresh-dependencies
```

#### Error: "Manifest merger failed"
**Cause**: Conflicting manifest declarations  
**Solution**: Check the error details in the Build panel and resolve conflicts in `AndroidManifest.xml`

### Runtime Issues

#### App crashes on startup
**Check**:
1. Logcat panel (View → Tool Windows → Logcat)
2. Look for red error messages
3. Common causes:
   - Missing permissions
   - Incompatible device API level

#### "Please configure your Hugging Face API key first"
**Solution**: 
- Go to Settings (⚙️ icon)
- Enter your API token
- Tap "Save API Key"

#### "Failed to get response" or Network errors
**Check**:
1. **Internet connection**: Device has active internet
2. **API token**: Correct and not expired
3. **API limits**: Hugging Face free tier has rate limits
4. **Model status**: Check [status.huggingface.co](https://status.huggingface.co/)

#### API returns error message
**Common errors**:
- **"Model is loading"**: Wait 20-30 seconds and try again
- **"Unauthorized"**: API token is invalid or expired
- **"Rate limit exceeded"**: Wait a few minutes before trying again

## Development Tips

### Enable Auto-Import
1. Go to **File → Settings → Editor → General → Auto Import**
2. Enable **"Add unambiguous imports on the fly"**

### Code Style
The project uses Kotlin coding conventions:
- Go to **File → Settings → Editor → Code Style → Kotlin**
- Set from: **"Kotlin style guide"**

### Debugging
1. Set breakpoints by clicking left margin of code editor
2. Click **Debug** button (bug icon) instead of Run
3. Use **Logcat** to view system logs
4. Add custom logs: `Log.d("TAG", "message")`

### Hot Reload
When using Jetpack Compose:
1. Changes to UI code can be updated without full rebuild
2. Look for **"Apply Changes"** icon in toolbar
3. Or use **Ctrl+F10** (Windows/Linux) / **Cmd+F10** (Mac)

## Version Catalog Updates

All dependency versions are in `gradle/libs.versions.toml`:

```toml
[versions]
agp = "8.1.4"
kotlin = "1.9.0"
# ... other versions
```

To update a version:
1. Edit `gradle/libs.versions.toml`
2. Change the version number
3. Sync Gradle
4. Build and test

## Environment Variables (Optional)

For security, you can store API keys as environment variables:

### On macOS/Linux:
```bash
export HUGGING_FACE_API_KEY="your_token_here"
```

### On Windows:
```cmd
set HUGGING_FACE_API_KEY=your_token_here
```

### Access in code:
```kotlin
val apiKey = System.getenv("HUGGING_FACE_API_KEY")
```

## Additional Resources

- [Android Developer Documentation](https://developer.android.com/)
- [Jetpack Compose Tutorial](https://developer.android.com/jetpack/compose/tutorial)
- [Hugging Face API Documentation](https://huggingface.co/docs/api-inference/)
- [Kotlin Documentation](https://kotlinlang.org/docs/home.html)

## Getting Help

If you encounter issues:

1. Check the **BUILD.md** file for build instructions
2. Review **QUICKSTART.md** for quick setup
3. See **ARCHITECTURE.md** for code structure
4. Check **Logcat** for runtime errors
5. Open an issue on GitHub with:
   - Android Studio version
   - Build error messages
   - Logcat output
   - Device/emulator details

---

**Next Steps**: After successful setup, check out **QUICKSTART.md** to start using the app!
