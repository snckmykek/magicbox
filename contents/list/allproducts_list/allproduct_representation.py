from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from global_variables import LIST, USER
from sqlite_requests import sqlite_requests
from elements.longpress_button import LongpressButton
import time

Builder.load_file(r'contents/list/allproducts_list/allproduct_representation.kv')


class AllProductRepresentation(BoxLayout):
    """Element for List of all products.
    """

    def __init__(self, **kwargs):
        super(AllProductRepresentation, self).__init__(**kwargs)

        self.height = LIST.product_representation.height

        self.parent_allproducts = ObjectProperty
        self.parent_listrepresentation = ObjectProperty

        self.name = ''
        self.units = ''
        self.rating = 0
        self.average_rating = 0
        self.frequency_of_use = 0
        self.quality = 0
        self.last_use = 0
        self.note = ''
        self.average_price = 0
        self.last_price = 0
        self.current_price = 0
        self.quantity = 0
        self.selected = False

    def update_record_bd(self):

        self.selected = self.ids.selected.active

        if self.selected:
            self.last_use = round(time.time())
            self.frequency_of_use += 1

        if sqlite_requests.is_product_in_table('current_products', USER.name,
                                               self.name, self.parent_listrepresentation) is self.selected:
            return  # If called by creating of Product in on_pre_open of AllProductsList

        if sqlite_requests.is_product_in_table('personal_products', USER.name, self.name):
            sqlite_requests.sqlite_update_record('personal_products',
                                                 {
                                                     'frequency_of_use': self.frequency_of_use,
                                                     'last_use': self.last_use
                                                 },
                                                 {'user': USER.name, 'name': self.name})
        else:
            sqlite_requests.sqlite_fill_table('personal_products', self.name, self.units, user=USER.name,
                                              frequency_of_use=1, last_use=round(time.time()))

        if self.selected:
            sqlite_requests.sqlite_fill_table('current_products', self.name, self.units, user=USER.name,
                                              products_list=self.parent_listrepresentation, price=self.current_price,
                                              quantity=self.quantity, bought='False')
        else:
            sqlite_requests.sqlite_delete_record('current_products', name=self.name, user=USER.name,
                                                 products_list=self.parent_listrepresentation)

    def delete_product(self):
        sqlite_requests.sqlite_delete_record('global_products', name=self.name)
        sqlite_requests.sqlite_delete_record('personal_products', name=self.name, user=USER.name)

        self.parent_allproducts.delete_product_from_list(self)
