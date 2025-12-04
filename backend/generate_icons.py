import os
from PIL import Image, ImageDraw, ImageFont

# Configuration
TARGET_DIR = r"d:\thingsboard_envor\tea\frontend-uni\static\tabbar"
os.makedirs(TARGET_DIR, exist_ok=True)

# Colors
COLOR_NORMAL = "#6B7280"  # Gray
COLOR_ACTIVE = "#10B981"  # Emerald Green
SIZE = (64, 64)

# Icons to generate
ICONS = [
    {"name": "home", "symbol": "H"},
    {"name": "alarm", "symbol": "A"},
    {"name": "ai", "symbol": "AI"},
    {"name": "user", "symbol": "U"},
]

def create_icon(filename, color, text):
    img = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw circle background (optional, maybe just text/symbol)
    # draw.ellipse([4, 4, 60, 60], outline=color, width=2)
    
    # Draw symbol (simple text for now)
    # Load default font
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
        
    # Calculate text position (rough centering)
    # draw.text((20, 15), text, fill=color, font=font)
    
    # Draw a simple colored square/circle to represent the icon
    draw.rounded_rectangle([10, 10, 54, 54], radius=10, fill=None, outline=color, width=3)
    
    # Draw a letter in the middle
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((64-w)/2, (64-h)/2 - 2), text, fill=color, font=font)

    img.save(os.path.join(TARGET_DIR, filename))
    print(f"Generated {filename}")

def main():
    print(f"Generating icons in {TARGET_DIR}...")
    for icon in ICONS:
        # Normal state
        create_icon(f"{icon['name']}.png", COLOR_NORMAL, icon['symbol'])
        # Active state
        create_icon(f"{icon['name']}-active.png", COLOR_ACTIVE, icon['symbol'])
    print("Done.")

if __name__ == "__main__":
    main()
