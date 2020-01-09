from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from contents.list.elements.boxes import ProductsListRepresentation as ProductsListRepresentationClass
import global_variables
from sqlite_requests import sqlite_requests


class AddList(ModalView):

    def __init__(self, **kwargs):
        super(AddList, self).__init__(**kwargs)

        self.ids.add_but.height = global_variables.BUTTON_SIZE[0]
        self.ids.listname.height = global_variables.BUTTON_SIZE[0]

        self.parentlist = ''  # Object, which call this Object

    def add_list(self, text='No name'):  # Adds List (Product list) in List of Products list
        ProductsListRepresentation = ProductsListRepresentationClass()
        ProductsListRepresentation.ids.representation.text = str(text)

        sqlite_requests.sqlite_fill_table('lists', str(text), user=global_variables.USER)

        self.parentlist.ids.list_of_products_lists.add_widget(ProductsListRepresentation)
        self.dismiss()


class List(BoxLayout):
    """This class make main object (box, which will be placed in a box of Carousel) of mini-application 'List'.
    """

    Builder.load_file(r'contents/list/list.kv')

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)
        self.ids.addlist_but.size = global_variables.FLYING_BUTTON_SIZE
        self.ids.addlist_but.background_color = global_variables.FLYING_BUTTON_BACKGROUND_COLOR
        self.fill_list_of_products_lists()

    def fill_list_of_products_lists(self):
        lists = sqlite_requests.sqlite_read_table('lists')
        for current_list in lists:
            if current_list[0] == global_variables.USER:
                ListRepresentation = ProductsListRepresentationClass()
                ListRepresentation.ids.representation.text = current_list[1]
                self.ids.list_of_products_lists.add_widget(ListRepresentation)

    def open_AddList(self):
        window_AddList = AddList()
        window_AddList.parentlist = self  # Only for transfer List to AddList
        window_AddList.open()


ListBox = List()
