from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from sqlite_requests import sqlite_requests
from contents.list.list_representation import ListRepresentation
from global_variables import USER, WINDOW, BUTTON

Builder.load_file(r'contents/list/list_creator/main_box.kv')


class ListCreator(ModalView):

    def __init__(self, **kwargs):
        super(ListCreator, self).__init__(**kwargs)

        parentlist: object  # Object, which call this Object

    def add_list(self, text='No name'):  # Adds List (Product list) in List of Products list
        self.LR.ids.name.text = str(text)
        self.LR.parent_box = self.parentlist

        self.parentlist.ids.list_of_products_lists.add_widget(self.LR)

        sqlite_requests.sqlite_fill_table('lists', str(text), user=USER.name)

        self.dismiss()

    def on_pre_open(self):
        self.LR = ListRepresentation()  # Разбить на другой поток, так не будет лага
        self.ids.name = 'Some list'

