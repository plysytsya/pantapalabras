import random
from typing import Tuple

from pantapalabras.constants import RGB_COLOR_PALLET


class BlackWhiteSwitch:
    """Randomly invert black and white."""

    def __init__(self):
        """Initialize with default black-white combination."""
        self._color_a = RGB_COLOR_PALLET["black"]
        self._color_b = RGB_COLOR_PALLET["white"]

    def _switch(self):
        self._color_a = random.choice([RGB_COLOR_PALLET["black"], RGB_COLOR_PALLET["white"]])  # noqa S311
        self._color_b = (
            RGB_COLOR_PALLET["black"] if self._color_a == RGB_COLOR_PALLET["white"] else RGB_COLOR_PALLET["white"]
        )

    @property
    def color_a(self) -> Tuple[int, int, int]:
        """Return either black or white RGB-tuple."""
        self._switch()
        return self._color_a

    @property
    def color_b(self) -> Tuple[int, int, int]:
        """Return either black or white RGB-tuple as contrary of color_a."""
        return self._color_b
