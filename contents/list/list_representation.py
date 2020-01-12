from contents.list.products_list.main_box import ProductsList
from global_variables import LIST
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty

Builder.load_file(r'contents/list/list_representation.kv')


class ListRepresentation(BoxLayout):
    """Element for List of products lists.
    """

    def __init__(self, **kwargs):
        super(ListRepresentation, self).__init__(**kwargs)

        self.ProductsListBox = ProductsList()
        self.height = LIST.list_representation.height

        self.parent_box = ObjectProperty

    def open_products_list(self, name_of_list):
        self.ProductsListBox.parent_listrepresentation = name_of_list
        self.ProductsListBox.open()

    def open_ProductsList(self):
        self.open_products_list(self.ids.name.text)

        # if self.collide_point(touch.x, touch.y):  # only for selected object
        #     self.open_products_list(self.ids.name.text)
        # return super(ListRepresentation, self).on_touch_down(touch)

    def delete_list(self):
        self.parent_box.delete_list(self)
