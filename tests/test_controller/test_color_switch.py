from pantapalabras.constants import RGB_COLOR_PALLET
from pantapalabras.controller.color_switch import BlackWhiteSwitch


def test_black_white_switch():
    # Arrange
    color_switch = BlackWhiteSwitch()

    # Act
    colors_a = []
    for _ in range(500):
        color_a = color_switch.color_a
        color_b = color_switch.color_b
        colors_a.append(color_a)

        # Assert
        assert color_a != color_b
    assert RGB_COLOR_PALLET["white"] in colors_a
    assert RGB_COLOR_PALLET["black"] in colors_a
