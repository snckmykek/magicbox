USER = 'Admin'


#  Settings
from kivy.core.window import Window
WINDOW_SIZE = (Window.height, Window.width)

LIST_REPRESENTATION_SIZE = (round(WINDOW_SIZE[0] / 10), 0)  # width not used for now

PRODUCT_REPRESENTATION_SIZE = (round(WINDOW_SIZE[0] / 15), 0)  # width not used for now

BUTTON_SIZE = (round(WINDOW_SIZE[0] / 10), round(WINDOW_SIZE[1] / 10))  # width not used for now

FLYING_BUTTON_SIZE = (round(WINDOW_SIZE[0] / 10), round(WINDOW_SIZE[0] / 10))
FLYING_BUTTON_BACKGROUND_COLOR = (.88, .34, .09, 1)
