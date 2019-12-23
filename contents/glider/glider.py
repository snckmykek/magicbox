from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


class Glider(BoxLayout):
    Builder.load_file(r'contents\glider\glider.kv')


GliderBox = Glider()
