from kivy.uix.textinput import TextInput
from kivy.lang import Builder

Builder.load_file(r'elements/common_textinput.kv')


class CommonTextInput(TextInput):
    def __init__(self, **kwargs):
        super(CommonTextInput, self).__init__(**kwargs)
