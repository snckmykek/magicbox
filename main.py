__version__ = "0.0.1"

from kivy.app import App

# from kivy.config import Config
#
# Config.set('graphics', 'resizable', '1')
# Config.set('graphics', 'width', '360')
# Config.set('graphics', 'height', '640')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
# from contents import BudgetBox, GliderBox, ListBox, ProgressBox, RecipesBox
# import global_variables
import sqlite_requests


class MainBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MainBoxLayout, self).__init__(**kwargs)

    # def set_current_slide(self, button):
    #     ContentBox = self.ids.content_box
    #     if self.matching_slides_and_buttons[ContentBox.current_slide] != button:
    #         ContentBox.load_slide(list(self.matching_slides_and_buttons.keys())[
    #                                   list(self.matching_slides_and_buttons.values()).index(button)])
    #     button.state = 'down'
    #
    # def change_buttons_state(self, current_slide):
    #     for button in self.matching_slides_and_buttons.values():
    #         button.state = 'normal'
    #     self.matching_slides_and_buttons[current_slide].state = 'down'
    #
    # def auth(self):
    #     popup = Authorization()
    #     popup.open()


# class Authorization(Popup):
#
#     def __init__(self, **kwargs):
#         super(Authorization, self).__init__(**kwargs)
#         self.ids.username.height = global_variables.BUTTON_SIZE[0]
#         self.ids.close_but.height = global_variables.BUTTON_SIZE[0]
#         self.ids.make_db_but.height = global_variables.BUTTON_SIZE[0]
#
#     def save_user(self):
#         global_variables.USER = self.ids.username.text
#         self.dismiss()
#
#     def get_width(self):
#         self.ids.width_id.text = str(global_variables.WINDOW_SIZE)


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
        # self.root.matching_slides_and_buttons = {self.root.ids.budget_box: self.root.ids.toggle_button_budget,
        #                                          self.root.ids.recipes_box: self.root.ids.toggle_button_recipes,
        #                                          self.root.ids.progress_box: self.root.ids.toggle_button_progress,
        #                                          self.root.ids.list_box: self.root.ids.toggle_button_list,
        #                                          self.root.ids.glider_box: self.root.ids.toggle_button_glider}
        #
        # self.root.matching_slides_and_contents = {self.root.ids.budget_box: BudgetBox,
        #                                           self.root.ids.recipes_box: RecipesBox,
        #                                           self.root.ids.progress_box: ProgressBox,
        #                                           self.root.ids.list_box: ListBox,
        #                                           self.root.ids.glider_box: GliderBox}
        #
        # for box in self.root.matching_slides_and_contents.keys():  # Add content-objects from contents to boxes in Carousel
        #     box.add_widget(self.root.matching_slides_and_contents[box])


if __name__ == "__main__":
    MainScreenApp().run()
