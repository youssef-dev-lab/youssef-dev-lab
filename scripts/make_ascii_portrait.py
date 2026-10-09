
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from pathlib import Path
from html import escape
import math
import random

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "portrait.png"
OUTPUT = ROOT / "ascii-portrait.svg"

# Portrait resolution
COLS = 100
ROWS = 95

# Character spacing
CELL_W = 8
CELL_H = 11

WIDTH = COLS * CELL_W + 40
HEIGHT = ROWS * CELL_H + 90

# Terminal theme
BG = "#0d1117"
CYAN = "#36cfff"
BRIGHT = "#b8f5ff"
GREEN = "#3fb950"

# Dark-to-light character density
CHARS = "    .:-=+*#%@"

random.seed(42)


def prepare_image():
    image = Image.open(SOURCE).convert("RGB")

    w, h = image.size

    # Include the full head and upper body
    image = image.crop((
        int(w * 0.05),
        int(h * 0.02),
        int(w * 0.95),
        int(h * 0.88)
    ))

    image = image.resize(
        (COLS, ROWS),
        Image.Resampling.LANCZOS
    )

    gray = ImageOps.grayscale(image)
    gray = ImageEnhance.Contrast(gray).enhance(1.65)
    gray = ImageEnhance.Sharpness(gray).enhance(1.5)

    return gray


def make_foreground_mask(image):
    """
    Create a soft mask around the subject.
    Keeps the portrait visible while fading
    the background toward the edges.
    """

    mask = Image.new("L", (COLS, ROWS))
    pixels = mask.load()

    for y in range(ROWS):
        for x in range(COLS):

            nx = (x - COLS / 2) / (COLS / 2)
            ny = (y - ROWS * 0.52) / (ROWS * 0.60)

            # Elliptical fading
            distance = math.sqrt(
                (nx / 0.95) ** 2 +
                (ny / 1.05) ** 2
            )

            fade = max(0, min(1, (1.12 - distance) / 0.35))

            pixels[x, y] = int(fade * 255)

    mask = mask.filter(ImageFilter.GaussianBlur(3))

    return mask


def generate_svg(gray, mask):
    parts = []

    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
    )

    parts.append(f"""
<rect width="100%" height="100%" fill="{BG}"/>

<text x="22" y="34"
      fill="{GREEN}"
      font-family="monospace"
      font-weight="bold"
      font-size="18">
youssef@github:~$
</text>

<text x="225" y="34"
      fill="#c9d1d9"
      font-family="monospace"
      font-size="18">
./portrait.sh
</text>

<style>
.ascii {{
    font-family: monospace;
    font-size: 11px;
    font-weight: bold;
}}

.spark {{
    animation: twinkle 3s ease-in-out infinite alternate;
}}

@keyframes twinkle {{
    from {{ opacity: .08; }}
    to {{ opacity: .55; }}
}}
</style>
""")

    # Subtle background sparkles
    for i in range(100):
        x = random.randint(15, WIDTH - 15)
        y = random.randint(75, HEIGHT - 20)

        size = random.choice([1, 1, 1, 2])

        delay = random.uniform(0, 3)

        parts.append(f"""
<circle class="spark"
        cx="{x}" cy="{y}"
        r="{size}"
        fill="{CYAN}"
        opacity=".2"
        style="animation-delay:{delay:.2f}s"/>
""")

    # Render ASCII portrait with progressive drawing
    for y in range(ROWS):
        for x in range(COLS):

            brightness = gray.getpixel((x, y))
            opacity = mask.getpixel((x, y)) / 255

            # Keep more facial detail
            value = (brightness / 255) ** 0.78

            index = int(value * (len(CHARS) - 1))
            char = CHARS[index]

            if char == " ":
                continue

            if opacity < 0.06:
                continue

            # Additional soft fade
            final_opacity = opacity * (
                0.45 + 0.55 * value
            )

            pos_x = 20 + x * CELL_W
            pos_y = 72 + y * CELL_H

            # Left-to-right, then top-to-bottom
            delay = (
                y * COLS + x
            ) / (ROWS * COLS) * 6

            color = BRIGHT if value > 0.75 else CYAN

            # 8 seconds: draw, hold, repeat
            t1 = delay / 8
            t2 = min((delay + 0.03) / 8, 0.999)

            parts.append(f"""
<text class="ascii"
      x="{pos_x}"
      y="{pos_y}"
      fill="{color}"
      opacity="0">
{escape(char)}
<animate
    attributeName="opacity"
    values="0;0;{final_opacity:.3f};{final_opacity:.3f}"
    keyTimes="0;{t1:.5f};{t2:.5f};1"
    dur="8s"
    repeatCount="indefinite"/>
</text>
""")

    parts.append("</svg>")

    OUTPUT.write_text(
        "\n".join(parts),
        encoding="utf-8"
    )


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Missing photograph: {SOURCE}"
        )

    gray = prepare_image()
    mask = make_foreground_mask(gray)

    generate_svg(gray, mask)

    print("ASCII portrait generated successfully!")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
