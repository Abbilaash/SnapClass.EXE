#!/usr/bin/env python3
"""
Create placeholder asset images for MSIX packaging
This script generates basic placeholder images for the Microsoft Store submission
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_placeholder_image(size, text, filename, bg_color=(70, 130, 180), text_color=(255, 255, 255)):
    """Create a placeholder image with text"""
    # Create image
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default
    try:
        # Calculate font size based on image size
        font_size = min(size) // 10
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Wrap text to fit image
    lines = textwrap.wrap(text, width=15)
    
    # Calculate text position (center)
    bbox = draw.multiline_textbbox((0, 0), '\n'.join(lines), font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.multiline_text((x, y), '\n'.join(lines), font=font, fill=text_color, align='center')
    
    # Save image
    img.save(filename)
    print(f"✅ Created: {filename}")

def main():
    """Create all required asset images"""
    # Create Assets directory if it doesn't exist
    assets_dir = "Assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"📁 Created Assets directory: {assets_dir}")
    
    # Define required assets
    assets = [
        # Store Logo (50x50)
        ((50, 50), "SnapClass\nStore Logo", "StoreLogo.png"),
        
        # Square 150x150 Logo
        ((150, 150), "SnapClass\nAI\n150x150", "Square150x150Logo.png"),
        
        # Square 44x44 Logo
        ((44, 44), "SC\n44x44", "Square44x44Logo.png"),
        
        # Wide 310x150 Logo
        ((310, 150), "SnapClass AI\nAdvanced Edge AI for Education", "Wide310x150Logo.png"),
        
        # Splash Screen (620x300)
        ((620, 300), "SnapClass AI\n\nAdvanced On-Device Edge AI\nfor Classroom Environments\n\nPowered by Snapdragon Hexagon NPU", "SplashScreen.png"),
    ]
    
    print("🎨 Creating MSIX asset images...")
    
    for size, text, filename in assets:
        filepath = os.path.join(assets_dir, filename)
        create_placeholder_image(size, text, filepath)
    
    print("\n🎉 All MSIX assets created successfully!")
    print("📁 Assets location: ./Assets/")
    print("\n📋 Next steps:")
    print("   1. Review the generated images")
    print("   2. Replace with your actual app icons and graphics")
    print("   3. Ensure images meet Microsoft Store requirements")
    print("   4. Run the MSIX build script")

if __name__ == "__main__":
    main()
