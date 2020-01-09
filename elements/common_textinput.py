from kivy.uix.button import Button
from kivy.lang import Builder


class CommonTextInput(Button):
    def __init__(self, **kwargs):
        super(CommonTextInput, self).__init__(**kwargs)

        Builder.load_file(r'elements/common_textinput.kv')
