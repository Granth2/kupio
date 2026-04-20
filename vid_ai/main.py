from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os

# ===== CONFIG =====
IMAGE_DIR = "images"
OUTPUT_DIR = "output"
VIDEO_NAME = "product_video.mp4"
SLIDE_DURATION = 3  # seconds per image
FONT_SIZE = 40
TEXT_BG_PADDING = 20

# ==================

os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_slide(image_path, text):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    draw = ImageDraw.Draw(img)

    # Try common fonts, fallback if not found
    try:
        font = ImageFont.truetype("Arial.ttf", FONT_SIZE)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", FONT_SIZE)
        except:
            font = ImageFont.load_default()

    text_width, text_height = draw.textsize(text, font=font)

    x = (width - text_width) // 2
    y = height - text_height - 60

    # Background rectangle for readability
    draw.rectangle(
        [
            x - TEXT_BG_PADDING,
            y - TEXT_BG_PADDING,
            x + text_width + TEXT_BG_PADDING,
            y + text_height + TEXT_BG_PADDING,
        ],
        fill=(0, 0, 0),
    )

    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    temp_path = f"temp_{os.path.basename(image_path)}"
    img.save(temp_path)

    clip = ImageClip(temp_path).set_duration(SLIDE_DURATION)
    clip = clip.fadein(0.5).fadeout(0.5)

    return clip


def create_video(texts):
    images = sorted(os.listdir(IMAGE_DIR))
    clips = []

    for img, text in zip(images, texts):
        img_path = os.path.join(IMAGE_DIR, img)
        clips.append(make_slide(img_path, text))

    final_video = concatenate_videoclips(clips, method="compose")

    output_path = os.path.join(OUTPUT_DIR, VIDEO_NAME)
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio=False,
    )

    print(f"\n✅ Video created at: {output_path}\n")


if __name__ == "__main__":
    product_text = [
        "Premium Build Quality",
        "Modern Minimal Design",
        "Durable and Reliable Performance"
    ]

    create_video(product_text)
