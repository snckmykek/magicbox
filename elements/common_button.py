from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_file(r'elements/common_button.kv')


class CommonButton(Button):
    def __init__(self, **kwargs):
        super(CommonButton, self).__init__(**kwargs)
