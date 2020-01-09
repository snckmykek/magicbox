__version__ = "0.0.1"

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MainBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainBoxLayout, self).__init__(**kwargs)


class MainScreenApp(App):
    """"Every content-object (mini-application) is in a separate box of Carousel.

    """

    def build(self):
        for i in range(500):
            a = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
            a.add_widget(Label(text=str(i), color=(1, 0, 0, 1),
                               size_hint_y=None, height=100))
            a.add_widget(Button(text=str(i), color=(1, 0, 0, 1),
                                size_hint_y=None, height=100))
            self.root.ids.products_list.add_widget(a)


if __name__ == "__main__":
    MainScreenApp().run()
