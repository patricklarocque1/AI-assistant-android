#!/usr/bin/env python3
"""
Simple script to generate placeholder launcher icons for Android
"""

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("PIL/Pillow not available, skipping icon generation")
    print("Icons will be generated from XML resources instead")
    exit(0)

import os

# Define icon sizes for different density folders
SIZES = {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192
}

# Base directory
base_dir = '/home/runner/work/AI-assistant-android/AI-assistant-android/app/src/main/res'

def create_icon(size, folder):
    """Create a simple icon with AI text"""
    # Create image with blue background
    img = Image.new('RGB', (size, size), color='#2196F3')
    draw = ImageDraw.Draw(img)
    
    # Draw AI text in center
    font_size = size // 2
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "AI"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2 - font_size // 6)
    draw.text(position, text, fill='white', font=font)
    
    # Save icons
    folder_path = os.path.join(base_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    img.save(os.path.join(folder_path, 'ic_launcher.png'))
    img.save(os.path.join(folder_path, 'ic_launcher_round.png'))
    print(f"Created icons for {folder} ({size}x{size})")

def main():
    for folder, size in SIZES.items():
        create_icon(size, folder)
    print("All icons generated successfully!")

if __name__ == '__main__':
    main()
