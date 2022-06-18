from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from pantapalabras.config import settings
from pantapalabras.constants import FONTS_DIR
from pantapalabras.controller.color_switch import BlackWhiteSwitch

BLACK_WHITE_SWITCH = BlackWhiteSwitch()


def _create_image_from_texts(text_a: str, text_b: str) -> Image:
    """Create an image from a vocabulary word-pair.

    The images are adjusted to fit the screen-size of an M5Paper device (960x540).
    """
    image = Image.new("RGB", settings.M5PAPER_SCREEN_SIZE, color=BLACK_WHITE_SWITCH.color_a)
    drawing = _draw_middle_line(image)

    font, width_a, width_b = _adjust_font_size(drawing, text_a, text_b)

    horizontal_position_a = _center_horizontally(width_a)
    horizontal_position_b = _center_horizontally(width_b)
    vertical_position_a, vertical_position_b = _center_vertically()

    drawing.text(
        (horizontal_position_a, vertical_position_a), text_a, font=font, fill=BLACK_WHITE_SWITCH.color_b, anchor="ld"
    )
    drawing.text((horizontal_position_b, vertical_position_b), text_b, font=font, fill=BLACK_WHITE_SWITCH.color_b)
    return image.transpose(Image.ROTATE_270)


def _adjust_font_size(drawing, text_a, text_b) -> Tuple[FreeTypeFont, int, int]:
    """Find the smaller of the two biggest possible sizes and return it with the widths of the two texts.

    First find the biggest possible font-size so that each line fits horizontally into the screen .
    Apply the smaller one of the two to both texts as we want both to fit into the screen and have the same size.
    Finally measure the width for each line with the selected font.
    """
    font_a, width_a = _fit_text_to_screen(drawing, text_a)
    font_b, width_b = _fit_text_to_screen(drawing, text_b)
    if font_b.size < font_a.size:
        width_a = _measure_text_width(drawing, text_a, font_b)
        font = font_b
    else:
        width_b = _measure_text_width(drawing, text_b, font_a)
        font = font_a
    return font, width_a, width_b


def _draw_middle_line(image: Image) -> ImageDraw.ImageDraw:
    drawing = ImageDraw.Draw(image)
    horizontal_center = int(round(settings.M5PAPER_SCREEN_SIZE[1] / 2, 0))
    drawing.line(
        (0, horizontal_center, settings.M5PAPER_SCREEN_SIZE[0], horizontal_center), fill=BLACK_WHITE_SWITCH.color_b
    )
    return drawing


def _fit_text_to_screen(drawing: ImageDraw.ImageDraw, text: str) -> Tuple[FreeTypeFont, int]:
    """Decrease font size incrementally starting at MAX_FONT_SIZE until text fits horizontally."""
    font_size = settings.MAX_FONT_SIZE
    font = _initialize_font(font_size)
    width = _measure_text_width(drawing, text, font)
    while width > settings.M5PAPER_SCREEN_SIZE[0] - settings.SCREEN_BORDER:
        font = _initialize_font(font_size)
        width = _measure_text_width(drawing, text, font)
        font_size -= 1
    return font, width


def _center_horizontally(width: int) -> int:
    border_width = settings.M5PAPER_SCREEN_SIZE[0] - width
    return int(round(border_width / 2, 0))


def _center_vertically() -> Tuple[int, int]:
    """Assumes that the upper text_a is measured from below whereas text_b is measured from above."""
    vertical_middle = int(round(settings.M5PAPER_SCREEN_SIZE[1] / 2, 0))
    half_border_between_texts = int(round(settings.VERTICAL_BORDER_BETWEEN_TEXTS / 2, 0))
    vertical_position_a = vertical_middle - half_border_between_texts
    vertical_position_b = vertical_middle + half_border_between_texts
    return vertical_position_a, vertical_position_b


def _initialize_font(size=settings.MAX_FONT_SIZE) -> FreeTypeFont:
    font_path = str(FONTS_DIR / settings.FONT)
    return ImageFont.truetype(font_path, size)


def _measure_text_width(blank_drawing: ImageDraw.ImageDraw, text: str, font: FreeTypeFont) -> int:
    return blank_drawing.textsize(text, font)[0]
