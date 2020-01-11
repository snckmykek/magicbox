from kivy.lang.builder import Builder
from global_variables import LIST, USER
from sqlite_requests import sqlite_requests
from kivy.properties import ObjectProperty
from kivy.uix.carousel import Carousel

Builder.load_file(r'contents/list/products_list/product_representation.kv')


class ProductRepresentation(Carousel):
    """Element for List of products.
    """

    def __init__(self, **kwargs):
        super(ProductRepresentation, self).__init__(**kwargs)

        self.parent_productlist = ObjectProperty
        self.parent_listrepresentation = ObjectProperty

        self.height = LIST.product_representation.height
        self.name = ''
        self.units = ''
        self.price = 0
        self.quantity = 0
        self.bought = False

    def update_record_bd(self, is_bought_changed=False):
        if is_bought_changed:
            self.bought = self.ids.bought.active
            sqlite_requests.sqlite_update_record('current_products',
                                                 {
                                                     'bought': self.bought
                                                 },
                                                 {'user': USER.name, 'name': self.name,
                                                  'products_list': self.parent_listrepresentation})
            self.parent_productlist.sort_products_list()

            if self.ids.bought.active:
                self.ids.representation.strikethrough = True
                self.ids.representation.color = (.5, .5, .5, 1)
                self.ids.quantity.color = (.5, .5, .5, 1)
            else:
                self.ids.representation.strikethrough = False
                self.ids.representation.color = (0, 0, 0, 1)
                self.ids.quantity.color = (0, 0, 0, 1)

        else:
            pass

    def delete_product_from_list(self):
        if self.slides[1] == self.current_slide:
            self.parent_productlist.delete_product_from_list(self)

            sqlite_requests.sqlite_delete_record('current_products', name=self.name, user=USER.name,
                                                 products_list=self.parent_listrepresentation)

    def make_invisible_units(self):
        pass  # still think
        # color_quantity = list(self.ids.quantity.color)
        # color_units = list(self.ids.units.color)
        # if float(self.ids.quantity.text) == 0:
        #     color_quantity[3] = 0
        #     color_units[3] = 0
        # else:
        #     color_quantity[3] = 1
        #     color_units[3] = 1
        # self.ids.quantity.color = color_quantity
        # self.ids.units.color = color_units

