from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from pantapalabras.config import settings
from pantapalabras.constants import FONTS_DIR, RGB_COLOR_PALLET


def _create_image_from_texts(text_a: str, text_b: str) -> Image:
    image = Image.new("RGB", settings.M5PAPER_SCREEN_SIZE, color=RGB_COLOR_PALLET["white"])
    drawing = ImageDraw.Draw(image)

    font_a = _adjust_font_size(drawing, text_a)
    font_b = _adjust_font_size(drawing, text_b)
    font = font_a if font_a.size < font_b.size else font_b

    drawing.text((30, 10), text_a, font=font, fill=RGB_COLOR_PALLET["black"])
    drawing.text((30, 250), text_b, font=font, fill=RGB_COLOR_PALLET["black"])
    return image.transpose(Image.ROTATE_270)


def _adjust_font_size(drawing: ImageDraw.ImageDraw, text: str) -> FreeTypeFont:
    font_size = settings.MAX_FONT_SIZE
    font = _initialize_font(font_size)
    width, height = _measure_text_size(drawing, text, font)
    while width > settings.M5PAPER_SCREEN_SIZE[0] - settings.SCREEN_BORDER:
        font = _initialize_font(font_size)
        width, height = _measure_text_size(drawing, text, font)
        font_size -= 1
    return font


def _initialize_font(size=settings.MAX_FONT_SIZE) -> FreeTypeFont:
    font_path = str(FONTS_DIR / settings.FONT)
    return ImageFont.truetype(font_path, size)


def _measure_text_size(blank_drawing: ImageDraw.ImageDraw, text: str, font: FreeTypeFont) -> Tuple[int, int]:
    return blank_drawing.textsize(text, font)
