import os, re, aiohttp, aiofiles
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL
from XQUEEN import app


def clear(text):
    result = ""
    for word in text.split():
        if len(result) + len(word) < 60:
            result += " " + word
    return result.strip()


async def get_thumb(videoid):
    output_path = f"cache/{videoid}.png"
    if os.path.exists(output_path):
        return output_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        search = VideosSearch(url, limit=1)
        results = (await search.next())["result"][0]

        title = re.sub(r"\W+", " ", results.get("title", "No Title")).title()
        duration = results.get("duration", "00:00")
        thumbnail_url = results["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/tmp_{videoid}.png", "wb") as f:
                        await f.write(await resp.read())

        # Load images
        raw_thumb = Image.open(f"cache/tmp_{videoid}.png").convert("RGB")
        template = Image.open("XQUEEN/assets/thum.png").convert("RGBA")
        final_img = Image.new("RGBA", template.size, (0, 0, 0, 255))

        # Optional blurred background
        bg = raw_thumb.resize(template.size).filter(ImageFilter.GaussianBlur(10))
        final_img.paste(bg, (0, 0))

        # Paste template overlay
        final_img.paste(template, (0, 0), mask=template)

        # Create square crop from center
        width, height = raw_thumb.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        thumb_crop = raw_thumb.crop((left, top, left + min_dim, top + min_dim))

        # Resize and apply circular mask
        thumb_size = 390
        thumb_resized = thumb_crop.resize((thumb_size, thumb_size))
        mask = Image.new("L", (thumb_size, thumb_size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, thumb_size, thumb_size), fill=255)
        thumb_resized.putalpha(mask)

        # 🔥 Place it in the center of the white ring (dynamically)
        # ⚠️ These values depend on your template; adjust if you change template later
        ring_center_x, ring_center_y = 300, 360  # Estimated center of white ring
        thumb_x = ring_center_x - thumb_size // 2
        thumb_y = ring_center_y - thumb_size // 2
        final_img.paste(thumb_resized, (thumb_x, thumb_y), mask=thumb_resized)

        # Add title and other texts
        draw = ImageDraw.Draw(final_img)
        font_title = ImageFont.truetype("XQUEEN/assets/font.ttf", 45)
        font_tag = ImageFont.truetype("XQUEEN/assets/font2.ttf", 25)

        draw.text((630, 50), clear(title), fill="white", font=font_title)
        draw.text((530, 350), f"00:00 / {duration}", fill="white", font=font_tag)
        draw.text((1250, 810), "XQUEEN SERVER", fill="white", font=font_tag)

        # Save and cleanup
        final_img.convert("RGB").save(output_path)
        os.remove(f"cache/tmp_{videoid}.png")
        return output_path

    except Exception as e:
        print(f"[THUMB ERROR] - {e}")
        return YOUTUBE_IMG_URL
