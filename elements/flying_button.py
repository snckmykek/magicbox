from kivy.uix.button import Button
from kivy.lang import Builder


class FlyingButton(Button):
    def __init__(self, **kwargs):
        super(FlyingButton, self).__init__(**kwargs)

        Builder.load_file(r'elements/flying_button.kv')
