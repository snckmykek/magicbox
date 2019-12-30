from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from contents.list.elements.boxes import ProductsListRepresentation as ProductsListRepresentationClass
import global_variables


class AddList(ModalView):

    def __init__(self, **kwargs):
        super(AddList, self).__init__(**kwargs)

        self.parentlist = ''  # Object, which call this Object

    def add_list(self, text='No name'):  # Adds List (Product list) in List of Products list
        ProductsListRepresentation = ProductsListRepresentationClass()
        ProductsListRepresentation.ids.representation.text = str(text)
        self.parentlist.ids.list_of_products_lists.add_widget(ProductsListRepresentation)
        self.dismiss()


class List(BoxLayout):
    """This class make main object (box, which will be placed in a box of Carousel) of mini-application 'List'.
    """

    Builder.load_file(r'contents/list/list.kv')

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)

    def fill_list_of_products_lists(self):
        pass
        # for _list in range(10):  # Test
            # ProductsListRepresentation = ProductsListRepresentationClass()
            # ProductsListRepresentation.ids.representation.text = str(_list)
            # self.ids.list_of_products_lists.add_widget(ProductsListRepresentation)

    def open_AddList(self):
        window_AddList = AddList()
        window_AddList.parentlist = self  # Only for transfer List to AddList
        window_AddList.open()


ListBox = List()
ListBox.fill_list_of_products_lists()
