import pytest
from PIL import Image, ImageDraw

from pantapalabras.config import settings
from pantapalabras.constants import RGB_COLOR_PALLET
from pantapalabras.controller.image_controller import (
    _adjust_font_size,
    _adjust_horizontal_position,
    _measure_text_size,
)


@pytest.mark.parametrize(
    "text",
    [
        "Hello, world!",
        "pariatur. Excepteur sint",
        "adipisci velit, sed quia non numquam",
        "magni",
        "voluptatem",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
    ],
)
def test_fit_text_to_screen(text: str):
    # Arrange
    image = Image.new("RGB", settings.M5PAPER_SCREEN_SIZE, color=RGB_COLOR_PALLET["white"])
    drawing = ImageDraw.Draw(image)

    # Act
    font, _, _ = _adjust_font_size(drawing, text)

    # Assert
    width, height = _measure_text_size(drawing, text, font)
    assert width <= settings.M5PAPER_SCREEN_SIZE[0] - settings.SCREEN_BORDER
    assert height <= settings.M5PAPER_SCREEN_SIZE[1] - settings.SCREEN_BORDER


@pytest.mark.parametrize(
    "text",
    [
        "Hello, world!",
        "pariatur. Excepteur sint",
        "adipisci velit, sed quia non numquam",
        "magni",
        "voluptatem",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
    ],
)
def test_centralize_text(text: str):
    # Arrange
    image = Image.new("RGB", settings.M5PAPER_SCREEN_SIZE, color=RGB_COLOR_PALLET["white"])
    drawing = ImageDraw.Draw(image)
    font, text_width, text_height = _adjust_font_size(drawing, text)

    # Act
    horizontal_position = _adjust_horizontal_position(text_width)

    # Assert
    assert isinstance(horizontal_position, int)
    assert horizontal_position > 0
    border_width = settings.M5PAPER_SCREEN_SIZE[0] - text_width
    half_border_width = int(round(border_width / 2, 0))
    assert horizontal_position == half_border_width
