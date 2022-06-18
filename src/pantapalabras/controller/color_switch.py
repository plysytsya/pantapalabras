from typing import Tuple

from pantapalabras.constants import RGB_COLOR_PALLET
from pantapalabras.schemas.vocabulary import User

USER_SWITCH_STATES = {}


class BlackWhiteSwitch:
    """Randomly invert black and white."""

    def __init__(self, user: User):
        """Initialize with color combination from USER_SWITCH_STATES or by default."""
        self._color_a = USER_SWITCH_STATES.get(user.id, RGB_COLOR_PALLET["black"])
        self._user = user

    def switch(self):
        """Switch between black and white."""
        if USER_SWITCH_STATES.get(self._user.id) == RGB_COLOR_PALLET["white"]:
            USER_SWITCH_STATES[self._user.id] = RGB_COLOR_PALLET["black"]
        else:
            USER_SWITCH_STATES[self._user.id] = RGB_COLOR_PALLET["white"]

    @property
    def color_a(self) -> Tuple[int, int, int]:
        """Return either black or white RGB-tuple."""
        return self._color_a

    @property
    def color_b(self) -> Tuple[int, int, int]:
        """Return either black or white RGB-tuple as contrary of color_a."""
        if self._color_a == RGB_COLOR_PALLET["white"]:
            return RGB_COLOR_PALLET["black"]
        else:
            return RGB_COLOR_PALLET["white"]
