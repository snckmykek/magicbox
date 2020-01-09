from contents.list.products_list.main_box import ProductsList
from global_variables import LIST
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

Builder.load_file(r'contents/list/list_representation.kv')


class ListRepresentation(BoxLayout):
    """Element for List of products lists.
    """

    def __init__(self, **kwargs):
        super(ListRepresentation, self).__init__(**kwargs)

        self.ProductsListBox = ProductsList()
        self.height = LIST.list_representation.height

    def open_products_list(self, name_of_list):
        self.ProductsListBox.parent_listrepresentation = name_of_list
        self.ProductsListBox.open()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):  # only for selected object
            self.open_products_list(self.ids.representation.text)
        return super(ListRepresentation, self).on_touch_down(touch)
