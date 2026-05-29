"""Generate colored-initials avatar JPEGs for individuals."""

import colorsys
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
INDIVIDUALS_JSON = REPO_ROOT / "demography" / "individuals.json"
OUT_DIR = REPO_ROOT / "demography" / "images"

SIZE = 128


def color_for_name(name: str) -> tuple[int, int, int]:
    h_int = int(hashlib.md5(name.encode("utf-8")).hexdigest()[:6], 16)
    hue = (h_int % 360) / 360.0
    r, g, b = colorsys.hls_to_rgb(hue, 0.45, 0.55)
    return int(r * 255), int(g * 255), int(b * 255)


def initials(first: str, last: str) -> str:
    f = (first or "")[:1].upper()
    l = (last or "")[:1].upper()
    return (f + l) or "?"


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def render(initials_text: str, color: tuple[int, int, int], out_path: Path) -> None:
    img = Image.new("RGB", (SIZE, SIZE), color)
    draw = ImageDraw.Draw(img)
    font = load_font(56)
    bbox = draw.textbbox((0, 0), initials_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (SIZE - tw) // 2 - bbox[0]
    y = (SIZE - th) // 2 - bbox[1]
    draw.text((x, y), initials_text, fill=(255, 255, 255), font=font)
    img.save(out_path, "JPEG", quality=85, optimize=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    individuals = json.loads(INDIVIDUALS_JSON.read_text())

    for ind in individuals:
        initials_text = initials(ind["first_name"], ind["last_name"])
        full_name = ind["full_name"]
        color = color_for_name(full_name)
        out_path = OUT_DIR / Path(ind["image_file"]).name
        render(initials_text, color, out_path)

    print(f"Wrote {len(individuals)} avatars to {OUT_DIR}")


if __name__ == "__main__":
    main()
