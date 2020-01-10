__version__ = "0.0.1"

from kivy.app import App

from kivy.config import Config

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.lang.builder import Builder
Builder.load_file('elements/import_elements.kv')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from contents import BudgetBox, GliderBox, ListBox, ProgressBox, RecipesBox
from global_variables import TEXTINPUT, BUTTON, WINDOW, USER


class MainBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainBoxLayout, self).__init__(**kwargs)

    def set_current_slide(self, button):
        ContentBox = self.ids.content_box
        if self.matching_slides_and_buttons[ContentBox.current_slide] != button:
            ContentBox.load_slide(list(self.matching_slides_and_buttons.keys())[
                                      list(self.matching_slides_and_buttons.values()).index(button)])
        button.state = 'down'

    def change_buttons_state(self, current_slide):
        for button in self.matching_slides_and_buttons.values():
            button.state = 'normal'
        self.matching_slides_and_buttons[current_slide].state = 'down'

    def auth(self):  # Каждый раз новый объект. Запихнуть в init када буду делать авторизацию
        popup = Authorization()
        popup.open()


class Authorization(Popup):

    def __init__(self, **kwargs):
        super(Authorization, self).__init__(**kwargs)
        self.ids.username.height = TEXTINPUT.common_textinput.height
        self.ids.close_but.height = BUTTON.common_button.height

    def save_user(self):
        USER.name = self.ids.username.text
        self.dismiss()

    def get_width(self):
        self.ids.width_id.text = str(WINDOW.size)


class MainScreenApp(App):
    """"Every content-object (mini-application) is in a separate box of Carousel.

    """

    def build(self):
        self.root.matching_slides_and_buttons = {self.root.ids.budget_box: self.root.ids.toggle_button_budget,
                                                 self.root.ids.recipes_box: self.root.ids.toggle_button_recipes,
                                                 self.root.ids.progress_box: self.root.ids.toggle_button_progress,
                                                 self.root.ids.list_box: self.root.ids.toggle_button_list,
                                                 self.root.ids.glider_box: self.root.ids.toggle_button_glider}

        self.root.matching_slides_and_contents = {self.root.ids.budget_box: BudgetBox,
                                                  self.root.ids.recipes_box: RecipesBox,
                                                  self.root.ids.progress_box: ProgressBox,
                                                  self.root.ids.list_box: ListBox,
                                                  self.root.ids.glider_box: GliderBox}

        for box in self.root.matching_slides_and_contents.keys():  # Add content-objects from contents to boxes in Carousel
            box.add_widget(self.root.matching_slides_and_contents[box])

        self.root.ids.content_box.load_slide(list(self.root.matching_slides_and_buttons.keys())[2])


if __name__ == "__main__":
    MainScreenApp().run()
