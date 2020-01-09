from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from contents.list.list_representation import ListRepresentation
from global_variables import USER
from sqlite_requests import sqlite_requests
from contents.list.list_creator.main_box import ListCreator


class List(BoxLayout):
    """This class make main object (box, which will be placed in a box of Carousel) of mini-application 'List'.
    """

    Builder.load_file(r'contents/list/main_page.kv')

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)
        self.fill_list_of_products_lists()
        self.list_creator = ListCreator()

    def fill_list_of_products_lists(self):  # Переделать
        lists = sqlite_requests.sqlite_read_table('lists')
        for current_list in lists:
            if current_list[0] == USER.name:
                LR = ListRepresentation()
                LR.ids.representation.text = current_list[1]
                self.ids.list_of_products_lists.add_widget(LR)

    def open_ListCreator(self):
        self.list_creator.parentlist = self  # Only for transfer List to ListCreator
        self.list_creator.open()


ListBox = List()
