import pytest
from PIL import Image, ImageDraw

from pantapalabras.config import settings
from pantapalabras.constants import RGB_COLOR_PALLET
from pantapalabras.controller.image_controller import _center_horizontally, _fit_text_to_screen, _measure_text_width

EXAMPLE_TEXTS = [
    "Hello, world!",
    "pariatur. Excepteur sint",
    "adipisci velit, sed quia non numquam",
    "magni",
    "voluptatem",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
]


@pytest.mark.parametrize(
    "text",
    EXAMPLE_TEXTS,
)
def test_fit_text_to_screen(text: str):
    # Arrange
    image = Image.new("RGB", settings.M5PAPER_SCREEN_SIZE, color=RGB_COLOR_PALLET["white"])
    drawing = ImageDraw.Draw(image)

    # Act
    font, _ = _fit_text_to_screen(drawing, text)

    # Assert
    width = _measure_text_width(drawing, text, font)
    assert width <= settings.M5PAPER_SCREEN_SIZE[0] - settings.SCREEN_BORDER


@pytest.mark.parametrize(
    "text",
    EXAMPLE_TEXTS,
)
def test_center_horizontally(text: str):
    # Arrange
    image = Image.new("RGB", settings.M5PAPER_SCREEN_SIZE, color=RGB_COLOR_PALLET["white"])
    drawing = ImageDraw.Draw(image)
    font, text_width = _fit_text_to_screen(drawing, text)

    # Act
    horizontal_position = _center_horizontally(text_width)

    # Assert
    assert isinstance(horizontal_position, int)
    assert horizontal_position > 0
    border_width = settings.M5PAPER_SCREEN_SIZE[0] - text_width
    half_border_width = int(round(border_width / 2, 0))
    assert horizontal_position == half_border_width
