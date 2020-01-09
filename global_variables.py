from typing import NamedTuple
from kivy.core.window import Window


# User
class UserInfo:
    name: str

    def __init__(self):
        self.name = 'Admin'
# end User


# Window
class WindowSettings:
    size: tuple
    width: int
    height: int

    def __init__(self):
        self.width = Window.width
        self.height = Window.height
        self.size = (self.width, self.height)
# end Window


# List
class ListSettings:
    list_representation: object
    product_representation: object

    def __init__(self):
        self.list_representation = ListRepresentation()
        self.product_representation = ProductRepresentation()


class ListRepresentation:
    size: tuple  # width, height
    width: int
    height: int
    spacing: int

    def __init__(self):
        self.width = 0  # width not used for now
        self.height = round(WINDOW.height / 10)
        self.size = (self.width, self.height)
        self.spacing = round(WINDOW.height / 370)


class ProductRepresentation:
    size: tuple  # width, height
    width: int
    height: int

    def __init__(self):
        self.width = 0  # width not used for now
        self.height = round(WINDOW.height / 15)
        self.size = (self.width, self.height)
# end List


# Button
class ButtonSettings:
    common_button: object
    flying_button: object

    def __init__(self):
        self.common_button = CommonButton()
        self.flying_button = FlyingButton()


class CommonButton:
    size: tuple  # width, height
    width: int
    height: int

    def __init__(self):
        self.width = round(WINDOW.width / 10)
        self.height = round(WINDOW.height / 10)
        self.size = (self.width, self.height)


class FlyingButton:
    size: tuple  # width, height
    width: int
    height: int
    diameter: int
    background_color: tuple

    def __init__(self):
        self.width = round(WINDOW.height / 10)
        self.height = round(WINDOW.height / 10)
        self.size = (self.width, self.height)
        self.diameter = round(WINDOW.height / 10)
# end Button


# TextInput
class TextInputSettings:
    common_textinput: object

    def __init__(self):
        self.common_textinput = CommonTextInput()


class CommonTextInput:
    size: tuple  # width, height
    width: int
    height: int

    def __init__(self):
        self.width = round(WINDOW.width / 10)
        self.height = round(WINDOW.height / 10)
        self.size = (self.width, self.height)
# end TextInput


USER = UserInfo()
WINDOW = WindowSettings()
LIST = ListSettings()
BUTTON = ButtonSettings()
TEXTINPUT = TextInputSettings()
