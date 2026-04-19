"""Generate the 1200x630 branded og:image for ki-agenten.shop.

Run this once; output is `og-image.jpg` in the repo root and committed.
Regenerate on brand changes.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).parent / "og-image.jpg"
W, H = 1200, 630

PETROL = (26, 99, 116)
PETROL_DARK = (18, 72, 85)
WHITE = (255, 255, 255)
ACCENT = (255, 255, 255, 40)

FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]


def font(path_hint: str, size: int) -> ImageFont.FreeTypeFont:
    for p in FONTS:
        if path_hint in p.lower():
            return ImageFont.truetype(p, size)
    return ImageFont.truetype(FONTS[0], size)


def build() -> None:
    img = Image.new("RGB", (W, H), PETROL)
    draw = ImageDraw.Draw(img, "RGBA")

    for y in range(H):
        t = y / H
        r = int(PETROL[0] * (1 - t * 0.35))
        g = int(PETROL[1] * (1 - t * 0.35))
        b = int(PETROL[2] * (1 - t * 0.35))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    for i in range(6):
        x = 80 + i * 180
        draw.ellipse((x - 40, 480 - i * 8, x + 40, 560 - i * 8), fill=ACCENT)

    draw.rectangle((80, 80, 120, 90), fill=WHITE)
    draw.text((140, 65), "ki-agenten.shop", font=font("bold", 42), fill=WHITE)

    title_font = font("bold", 84)
    sub_font = font("arial", 40)

    title = "DSGVO-konforme\nKI-Agenten"
    draw.multiline_text((80, 210), title, font=title_font, fill=WHITE, spacing=10)

    sub = "Master-KI, Agenten, Tools — zentral orchestriert."
    draw.text((80, 470), sub, font=sub_font, fill=(220, 240, 245))

    badges = ["EU-Hosting", "Datensouverän", "Mittelstand"]
    x = 80
    for b in badges:
        bbox = draw.textbbox((0, 0), b, font=font("arial", 26))
        w = bbox[2] - bbox[0] + 40
        draw.rounded_rectangle((x, 540, x + w, 585), radius=22, outline=WHITE, width=2)
        draw.text((x + 20, 548), b, font=font("arial", 26), fill=WHITE)
        x += w + 16

    img.save(OUT, "JPEG", quality=88, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
