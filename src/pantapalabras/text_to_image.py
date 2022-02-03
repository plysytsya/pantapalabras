from PIL import Image, ImageDraw, ImageFont

from pantapalabras.config import settings
from pantapalabras.constants import FONTS_DIR


def create_image_from_texts(text_a: str, text_b: str):
    image = Image.new("RGB", (960, 540), color=(255, 255, 255))
    drawing = ImageDraw.Draw(image)
    font = _initialize_font()

    drawing.text((10, 10), text_a, font=font, fill=(0, 0, 0))
    drawing.text((10, 250), text_b, font=font, fill=(0, 0, 0))
    return image.transpose(Image.ROTATE_90)


def _initialize_font(file_name=settings.FONT, size=150):
    font_path = str(FONTS_DIR / file_name)
    print(font_path)
    return ImageFont.truetype(font_path, size)


def _measure_text_size(blank_drawing, text, font):
    return blank_drawing.textsize(text, font)
