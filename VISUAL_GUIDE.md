# App Screenshots & Visual Guide

## Main Screens

### 1. Chat Screen (Default)

**What you'll see:**
- Top bar with "AI Assistant" title and Settings icon
- Welcome message from AI
- Your messages on the right (blue bubbles)
- AI responses on the left (gray bubbles)
- Message input field at bottom
- Send button (arrow icon)

**Features visible:**
- Message timestamps
- Auto-scroll to latest message
- Loading indicator when AI is responding
- Error messages (if any) at top

**User Actions:**
- Type message in input field
- Tap Send button to submit
- Scroll through message history
- Tap Settings icon for configuration

---

### 2. Settings Screen

**What you'll see:**
- Back arrow to return to chat
- "Settings" title
- Hugging Face Configuration section
- API Key input field (password protected)
- "Save API Key" button
- Chat Management section
- "Clear Chat History" button
- Model Information card

**Features visible:**
- Secure password field for API key
- Help text with website link
- Confirmation dialog for clearing chat
- Current AI model display

**User Actions:**
- Enter/update API key
- Save API key
- Clear all messages
- Return to chat

---

### 3. Welcome State (First Launch)

**What you'll see:**
- Empty chat screen
- Welcome message: "Hello! I'm your AI assistant powered by Hugging Face..."
- Settings icon prominently visible
- Clean, minimal interface

**User Actions:**
- First: Go to Settings and configure API key
- Then: Return and start chatting

---

## UI Elements Detail

### Message Bubble (User)
```
┌─────────────────────────┐
│ Your message text here  │
│ appears in blue         │
│                    10:30│
└─────────────────────────┘
```
- Aligned to right
- Blue/purple background (Material 3 primary)
- White text
- Timestamp in bottom right
- Rounded corners

### Message Bubble (AI)
```
┌─────────────────────────┐
│ AI response appears     │
│ here in gray            │
│ 10:30                   │
└─────────────────────────┘
```
- Aligned to left
- Gray background (Material 3 secondary)
- Dark text
- Timestamp in bottom left
- Rounded corners

### Input Field
```
┌─────────────────────────────────┬───┐
│ Type your message...            │ ➤ │
└─────────────────────────────────┴───┘
```
- Full width at bottom
- Rounded corners
- Send button on right
- Disabled when no text
- Disabled while loading

### Loading Indicator
```
        ⟳ Loading...
```
- Centered spinner
- Appears while waiting for AI response
- Below messages
- Animated

### Error Message
```
┌─────────────────────────────────────┐
│ ⚠️ Failed to get response.          │
│ Please try again.                   │
└─────────────────────────────────────┘
```
- Red background
- White text
- Full width at top
- Dismissible

---

## Color Scheme

### Light Mode (Default)
- **Primary**: Purple/Blue (#6650a4)
- **Secondary**: Gray/Purple (#625b71)
- **Background**: White/Light Gray
- **Text**: Dark Gray/Black
- **Error**: Red

### Dark Mode (System Default)
- **Primary**: Light Purple (#D0BCFF)
- **Secondary**: Light Gray (#CCC2DC)
- **Background**: Dark Gray/Black
- **Text**: White/Light Gray
- **Error**: Light Red

### Material You (Android 12+)
- Colors adapt to device wallpaper
- Dynamic color extraction
- System-wide theme consistency

---

## Typography

### Titles
- Font: System Default
- Weight: Medium/Bold
- Size: 22sp
- Usage: Screen titles, headers

### Body Text
- Font: System Default
- Weight: Regular
- Size: 16sp
- Usage: Messages, descriptions

### Labels
- Font: System Default
- Weight: Medium
- Size: 11sp
- Usage: Timestamps, hints

---

## Navigation Flow

```
┌─────────────────┐
│   Chat Screen   │ ←─────────────┐
│  (Default View) │                │
└────────┬────────┘                │
         │                         │
    Tap Settings                   │
         │                         │
         ▼                         │
┌─────────────────┐                │
│ Settings Screen │                │
│                 │                │
└────────┬────────┘                │
         │                         │
    Tap Back Arrow                 │
         │                         │
         └────────────────────────┘
```

**Simple two-screen navigation:**
- Chat ↔ Settings
- No complex navigation stack
- Back button always returns to chat

---

## Interactive Elements

### Buttons

**Primary Button** (Save API Key)
```
┌─────────────────────────┐
│    Save API Key         │
└─────────────────────────┘
```
- Filled background
- Prominent
- Full width

**Secondary Button** (Clear Chat)
```
┌─────────────────────────┐
│ 🗑️  Clear Chat History  │
└─────────────────────────┘
```
- Outlined style
- Icon included
- Full width

**Icon Button** (Settings)
```
  ⚙️
```
- Transparent background
- Small size
- In top bar

**Icon Button** (Send)
```
  ➤
```
- Circular
- Filled background
- Bottom right of input

### Text Fields

**Standard Input** (Message)
```
┌─────────────────────────┐
│ Type your message...    │
└─────────────────────────┘
```
- Rounded corners
- Light background
- Full width

**Password Input** (API Key)
```
┌─────────────────────────┐
│ ●●●●●●●●●●●●●●●●●●     │
└─────────────────────────┘
```
- Masked characters
- Rounded corners
- Full width

---

## Animations

### Message Appearance
- Fade in effect
- Smooth scroll to bottom
- Instant for user messages
- Delayed for AI responses

### Loading State
- Rotating spinner
- Pulsing effect
- Smooth transition

### Screen Transitions
- Slide in/out
- No jarring changes
- Smooth back navigation

---

## Accessibility

### Features
- **High contrast** color scheme
- **Large touch targets** (48dp minimum)
- **Clear labels** on all buttons
- **Readable fonts** (minimum 16sp)
- **TalkBack compatible**
- **Screen reader** support

### Content Descriptions
- All icons have descriptions
- Images have alt text
- Buttons announce their purpose
- Navigation is clear

---

## Responsive Design

### Phone (Portrait)
- Optimized for one-hand use
- Comfortable reading width
- Easy-to-reach controls

### Phone (Landscape)
- Wider message bubbles
- Better keyboard space
- Optimized layout

### Tablet
- Wider margins
- Larger text
- Better use of space

### Foldable Devices
- Adapts to screen changes
- Maintains state across fold
- Optimized for all modes

---

## Status Indicators

### Network Connection
- Automatic detection
- Error message if offline
- Retry option available

### API Status
- "Connecting..." during request
- "Waiting for response..." when processing
- Error messages for failures

### Input Status
- Disabled during loading
- Enabled when ready
- Visual feedback on tap

---

## User Feedback

### Success
- Message sent → Immediate display
- API key saved → Return to chat
- Chat cleared → Confirmation shown

### Error
- Network failure → Red banner
- Invalid API key → Error message
- Empty message → Button disabled

### Loading
- Spinner during AI response
- Disabled input during processing
- Visual indication of activity

---

## Best Practices Implemented

✅ **Consistent design** throughout app
✅ **Material 3** design guidelines
✅ **Responsive** to all screen sizes
✅ **Accessible** to all users
✅ **Clear feedback** for all actions
✅ **Smooth animations** for polish
✅ **Intuitive navigation** flow
✅ **Error handling** with helpful messages

---

For actual screenshots, build and run the app, then capture screens at different stages of use!
