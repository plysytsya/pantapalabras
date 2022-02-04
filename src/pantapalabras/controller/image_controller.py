from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from pantapalabras.config import settings
from pantapalabras.constants import FONTS_DIR, RGB_COLOR_PALLET


def _create_image_from_texts(text_a: str, text_b: str) -> Image:
    image = Image.new("RGB", settings.M5PAPER_SCREEN_SIZE, color=RGB_COLOR_PALLET["white"])
    drawing = ImageDraw.Draw(image)

    font_a, width_a, height_a = _adjust_font_size(drawing, text_a)
    font_b, width_b, height_b = _adjust_font_size(drawing, text_b)
    font = font_a if font_a.size < font_b.size else font_b

    horizontal_position_a = _adjust_horizontal_position(width_a)
    horizontal_position_b = _adjust_horizontal_position(width_b)
    print(horizontal_position_a, horizontal_position_b)

    drawing.text((horizontal_position_a, 10), text_a, font=font, fill=RGB_COLOR_PALLET["black"])
    drawing.text((horizontal_position_b, 250), text_b, font=font, fill=RGB_COLOR_PALLET["black"])
    return image  # .transpose(Image.ROTATE_270)


def _adjust_font_size(drawing: ImageDraw.ImageDraw, text: str) -> Tuple[FreeTypeFont, int, int]:
    font_size = settings.MAX_FONT_SIZE
    font = _initialize_font(font_size)
    width, height = _measure_text_size(drawing, text, font)
    while width > settings.M5PAPER_SCREEN_SIZE[0] - settings.SCREEN_BORDER:
        font = _initialize_font(font_size)
        width, height = _measure_text_size(drawing, text, font)
        font_size -= 1
    return font, width, height


def _adjust_horizontal_position(width: int) -> int:
    border_width = settings.M5PAPER_SCREEN_SIZE[0] - width
    return int(round(border_width / 2, 0))


def _initialize_font(size=settings.MAX_FONT_SIZE) -> FreeTypeFont:
    font_path = str(FONTS_DIR / settings.FONT)
    return ImageFont.truetype(font_path, size)


def _measure_text_size(blank_drawing: ImageDraw.ImageDraw, text: str, font: FreeTypeFont) -> Tuple[int, int]:
    return blank_drawing.textsize(text, font)
