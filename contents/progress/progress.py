from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


class Progress(BoxLayout):
    Builder.load_file(r'contents/progress/progress.kv')


ProgressBox = Progress()
