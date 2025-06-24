import os
import re
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL
from XQUEEN import app


def clear(text):
    """Limits text to approximately 60 characters to prevent overflow"""
    result = ""
    for word in text.split():
        if len(result) + len(word) < 60:
            result += " " + word
    return result.strip()


def create_circular_thumb(image, size):
    """Creates a perfect circular thumbnail with transparent background"""
    # Crop square from center
    width, height = image.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    crop = image.crop((left, top, left + min_dim, top + min_dim))

    # Resize
    crop = crop.resize((size, size))

    # Circular mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Apply mask to crop
    result = Image.new("RGBA", (size, size))
    result.paste(crop, (0, 0), mask=mask)
    return result


async def get_thumb(videoid):
    output_path = f"cache/{videoid}.png"
    if os.path.exists(output_path):
        return output_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        # Get video info from YouTube
        search = VideosSearch(url, limit=1)
        results = (await search.next())["result"][0]

        title = re.sub(r"\W+", " ", results.get("title", "No Title")).title()
        duration = results.get("duration", "00:00")
        thumbnail_url = results["thumbnails"][0]["url"].split("?")[0]

        # Download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/tmp_{videoid}.png", "wb") as f:
                        await f.write(await resp.read())

        # Load base images
        raw_thumb = Image.open(f"cache/tmp_{videoid}.png").convert("RGB")
        template = Image.open("XQUEEN/assets/thum.png").convert("RGBA")
        final_img = Image.new("RGBA", template.size, (0, 0, 0, 255))

        # Blur background
        bg = raw_thumb.resize(template.size).filter(ImageFilter.GaussianBlur(10))
        final_img.paste(bg, (0, 0))

        # Paste the player UI template
        final_img.paste(template, (0, 0), mask=template)

        # ✅ Create circular thumbnail (494px) and fit into white ring at exact center
        thumb_size = 494
        circular_thumb = create_circular_thumb(raw_thumb, thumb_size)

        # Perfect center position (based on your template test)
        ring_center_x, ring_center_y = 336, 432
        thumb_x = ring_center_x - thumb_size // 2
        thumb_y = ring_center_y - thumb_size // 2
        final_img.paste(circular_thumb, (thumb_x, thumb_y), circular_thumb)

        # Draw text elements
        draw = ImageDraw.Draw(final_img)
        font_title = ImageFont.truetype("XQUEEN/assets/font.ttf", 45)
        font_tag = ImageFont.truetype("XQUEEN/assets/font2.ttf", 25)

        # Video title
        title_text = clear(title)
        draw.text((630, 50), title_text, fill="white", font=font_title)

        # Duration
        draw.text((530, 350), f"00:00 / {duration}", fill="white", font=font_tag)

        # Footer
        draw.text((1250, 810), "XQUEEN SERVER", fill="white", font=font_tag)

        # Save and cleanup
        final_img.convert("RGB").save(output_path)
        os.remove(f"cache/tmp_{videoid}.png")
        return output_path

    except Exception as e:
        print(f"[THUMB ERROR] - {e}")
        return YOUTUBE_IMG_URL
