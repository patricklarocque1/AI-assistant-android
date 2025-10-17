# Troubleshooting Checklist

Quick reference for common issues when setting up and using the AI Assistant app.

## Build Issues

### ☑ Gradle Sync Failed

- [ ] Check internet connection
- [ ] Clear Gradle cache: `./gradlew clean --refresh-dependencies`
- [ ] Invalidate caches: File → Invalidate Caches / Restart in Android Studio
- [ ] Update Android Studio to latest version
- [ ] Check `gradle/libs.versions.toml` for correct versions

### ☑ SDK Not Found

- [ ] Go to File → Project Structure → SDK Location
- [ ] Set Android SDK path
- [ ] Install SDK via Tools → SDK Manager
- [ ] Install Build Tools 33.0.1+

### ☑ JDK Version Error

- [ ] Check File → Project Structure → SDK Location
- [ ] Set JDK to version 17 or higher (Java 21 recommended)
- [ ] Download JDK 21 from [adoptium.net](https://adoptium.net/)
- [ ] Project uses foojay toolchain resolver for automatic Java download

### ☑ Build Takes Too Long

- [ ] Enable Gradle daemon (should be default)
- [ ] Increase heap size in `gradle.properties`:
  ```properties
  org.gradle.jvmargs=-Xmx4096m
  ```
- [ ] Use `--no-daemon` for one-off builds
- [ ] Check for antivirus interference

### ☑ Windows File Locking Issues

**"Couldn't delete R.jar" or similar errors:**
- [ ] Stop Gradle daemons: `./gradlew --stop`
- [ ] Close Android Studio/IDE completely
- [ ] Clean build: `./gradlew clean`
- [ ] Try building again: `./gradlew build`
- [ ] Check for Windows Defender scanning files
- [ ] Add project folder to Windows Defender exclusions if needed

### ☑ AGP/Gradle Compatibility Issues

**Version mismatch errors:**
- [ ] Check AGP version in `gradle/libs.versions.toml` (should be 8.7.3)
- [ ] Check Gradle version in `gradle/wrapper/gradle-wrapper.properties` (should be 8.11.1)
- [ ] Ensure Kotlin version is 2.1.0 or compatible
- [ ] Use kotlin-compose plugin for Kotlin 2.0+ (already configured)

## Runtime Issues

### ☑ App Won't Install

- [ ] Check device has sufficient storage
- [ ] Uninstall previous version
- [ ] Enable "Install Unknown Apps" in device settings
- [ ] Check USB debugging is enabled
- [ ] Try: `adb uninstall com.aiassistant.chat`

### ☑ App Crashes on Startup

**Check Logcat** (View → Tool Windows → Logcat):
- [ ] Look for red error messages
- [ ] Check for missing permissions
- [ ] Verify device API level ≥ 24
- [ ] Check for resource not found errors

### ☑ Network/Internet Issues

- [ ] Device has active internet connection
- [ ] WiFi or mobile data is enabled
- [ ] Firewall not blocking app
- [ ] Proxy settings (if applicable)
- [ ] Check AndroidManifest has INTERNET permission

## API Connection Issues

### ☑ "Please configure your Hugging Face API key first"

- [ ] Open Settings (⚙️ icon)
- [ ] Enter your Hugging Face API token
- [ ] Tap "Save API Key"
- [ ] Token starts with `hf_`

### ☑ "Failed to get response"

**Invalid API Token:**
- [ ] Token copied correctly (no extra spaces)
- [ ] Token is still valid (check Hugging Face settings)
- [ ] Token has "Read" permission
- [ ] Generate new token if needed

**Network Issues:**
- [ ] Device has internet connection
- [ ] Try on different network (WiFi vs mobile)
- [ ] Check [status.huggingface.co](https://status.huggingface.co/)
- [ ] Wait and retry

**Rate Limits:**
- [ ] Free tier: 30 requests/hour
- [ ] Wait for rate limit reset
- [ ] Check usage at huggingface.co/settings/billing

### ☑ "Model is loading"

- [ ] Wait 20-30 seconds
- [ ] Try request again
- [ ] Normal on first request or after inactivity
- [ ] Model needs to "warm up"

### ☑ Slow Responses

- [ ] First request always slower (cold start)
- [ ] Large model (Mistral-7B) takes time
- [ ] Check internet speed
- [ ] Wait up to 30 seconds
- [ ] Consider using smaller/faster model

### ☑ "Unauthorized" Error

- [ ] API token is correct
- [ ] Token hasn't expired
- [ ] Token has proper permissions
- [ ] Generate new token

## Android Studio Issues

### ☑ Slow Performance

- [ ] Close unused projects
- [ ] Increase IDE memory: Help → Edit Custom VM Options
  ```
  -Xmx4096m
  ```
- [ ] Disable unused plugins
- [ ] Clear caches: File → Invalidate Caches

### ☑ Code Not Auto-Completing

- [ ] Wait for indexing to complete (progress bar)
- [ ] File → Invalidate Caches / Restart
- [ ] Check File → Project Structure is correct
- [ ] Sync Gradle files

### ☑ Version Catalog Not Recognized

- [ ] Check `gradle/libs.versions.toml` exists
- [ ] Sync Gradle: File → Sync Project with Gradle Files
- [ ] Restart Android Studio
- [ ] Check for syntax errors in toml file

## Device/Emulator Issues

### ☑ Emulator Won't Start

- [ ] Enable hardware acceleration (Intel HAXM or AMD)
- [ ] Check virtualization is enabled in BIOS
- [ ] Try cold boot: Device Manager → Cold Boot Now
- [ ] Delete and recreate emulator
- [ ] Use different system image

### ☑ Physical Device Not Detected

- [ ] USB debugging enabled on device
- [ ] Use official USB cable
- [ ] Try different USB port
- [ ] Install device drivers (Windows)
- [ ] Run: `adb devices` to check connection
- [ ] Revoke USB debugging authorizations and reconnect

### ☑ App Not Updating

- [ ] Clean build: Build → Clean Project
- [ ] Rebuild: Build → Rebuild Project
- [ ] Uninstall app from device
- [ ] Clear app data on device
- [ ] Invalidate caches and restart IDE

## Quick Fixes

### Fast Recovery Steps

1. **Clean and rebuild**:
   ```bash
   ./gradlew clean build
   ```

2. **Invalidate caches** (Android Studio):
   - File → Invalidate Caches / Restart

3. **Delete build folders**:
   ```bash
   rm -rf .gradle/
   rm -rf build/
   rm -rf app/build/
   ```

4. **Refresh dependencies**:
   ```bash
   ./gradlew build --refresh-dependencies
   ```

5. **Reset Gradle daemon**:
   ```bash
   ./gradlew --stop
   ```

## Getting Additional Help

### Before Asking for Help

Collect this information:
- [ ] Android Studio version
- [ ] Gradle version (check `gradle/wrapper/gradle-wrapper.properties`)
- [ ] AGP version (check `gradle/libs.versions.toml`)
- [ ] Device/Emulator: Model, API level
- [ ] Error messages (exact text)
- [ ] Logcat output (if runtime error)
- [ ] Build output (if build error)

### Where to Get Help

1. **Documentation**:
   - ANDROID_STUDIO_SETUP.md - Full setup guide
   - API_SETUP.md - API configuration
   - BUILD.md - Build instructions
   - ARCHITECTURE.md - Code structure

2. **Online Resources**:
   - [Android Developer Docs](https://developer.android.com/)
   - [Stack Overflow](https://stackoverflow.com/questions/tagged/android)
   - [Hugging Face Forums](https://discuss.huggingface.co/)

3. **Project Issues**:
   - Open GitHub issue
   - Include all information listed above
   - Attach screenshots if helpful

## Prevention Tips

### Keep Your Setup Current

- [ ] Update Android Studio regularly
- [ ] Update SDK tools via SDK Manager
- [ ] Check for Gradle updates
- [ ] Keep dependencies up to date in `libs.versions.toml`

### Best Practices

- [ ] Commit working code frequently
- [ ] Test on multiple devices/emulators
- [ ] Monitor Logcat during development
- [ ] Keep API keys secure (never commit)
- [ ] Document custom configurations

### Backup Configurations

Save these files (without secrets):
- `gradle/libs.versions.toml` - Dependencies
- `app/build.gradle.kts` - App configuration
- `local.properties` - SDK location (don't commit)

---

**Still stuck?** Check the comprehensive guides:
- ANDROID_STUDIO_SETUP.md
- API_SETUP.md
- Or open a GitHub issue with details
