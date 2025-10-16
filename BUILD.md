# Android AI Assistant - Build Guide

## Quick Start

### Option 1: Android Studio (Recommended)

1. Open Android Studio
2. Select "Open an Existing Project"
3. Navigate to this directory
4. Wait for Gradle sync to complete
5. Click Run (or Shift+F10)

### Option 2: Command Line

```bash
# On Linux/Mac
./gradlew assembleDebug

# On Windows
gradlew.bat assembleDebug
```

The APK will be generated at:
```
app/build/outputs/apk/debug/app-debug.apk
```

## Installing the APK

### Via ADB
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Via Android Studio
- Click Run and select your device

### Manual Installation
1. Transfer the APK to your device
2. Enable "Install from Unknown Sources" in Settings
3. Open the APK file to install

## Build Variants

### Debug Build
```bash
./gradlew assembleDebug
```
- Includes debugging symbols
- Allows debugging with Android Studio
- Larger APK size

### Release Build
```bash
./gradlew assembleRelease
```
- Optimized for production
- Requires signing configuration
- Smaller APK size

## Signing Configuration (for Release)

1. Create a keystore:
```bash
keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias
```

2. Add to `app/build.gradle.kts`:
```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("my-release-key.jks")
            storePassword = "your-store-password"
            keyAlias = "my-key-alias"
            keyPassword = "your-key-password"
        }
    }
    buildTypes {
        getByName("release") {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

## Troubleshooting Build Issues

### Gradle Sync Failed
1. Check internet connection (Gradle needs to download dependencies)
2. Clear Gradle cache:
   ```bash
   ./gradlew clean --refresh-dependencies
   ```
3. In Android Studio: File → Invalidate Caches / Restart

### Out of Memory
Add to `gradle.properties`:
```
org.gradle.jvmargs=-Xmx4096m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
```

### SDK Not Found
1. Open Android Studio → SDK Manager
2. Install Android SDK Platform 34
3. Install Android SDK Build-Tools 34.0.0

### Build Tools Version
If you get version errors, update in `app/build.gradle.kts`:
```kotlin
android {
    compileSdk = 34
    buildToolsVersion = "34.0.0"
}
```

## Testing

### Run Unit Tests
```bash
./gradlew test
```

### Run Instrumented Tests
```bash
./gradlew connectedAndroidTest
```

## Code Quality

### Lint Check
```bash
./gradlew lint
```

### Format Code
Enable Kotlin formatting in Android Studio:
- Settings → Editor → Code Style → Kotlin
- Set from: Kotlin style guide

## Clean Build

Remove all build artifacts:
```bash
./gradlew clean
```

## Build All Variants
```bash
./gradlew build
```

This will create both debug and release APKs.
