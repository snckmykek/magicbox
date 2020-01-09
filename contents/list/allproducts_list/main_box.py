from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from sqlite_requests import sqlite_requests
from global_variables import LIST, USER
from contents.list.allproducts_list.allproduct_representation import AllProductRepresentation
import time

Builder.load_file(r'contents/list/allproducts_list/main_box.kv')


class AllProductsList(ModalView):

    def __init__(self, **kwargs):
        super(AllProductsList, self).__init__(**kwargs)

        self.ids.all_products_list.spacing = LIST.list_representation.spacing

        self.parent_listrepresentation = ObjectProperty
        self.parent_productlist = ObjectProperty

        self.all_products = []
        self.current_products = []
        self.product_pages_to_show = 1  # how_many_product_pages_to_show*how_many_products_to_show
        self.products_to_show = 10
        self.sort = 'popular'  # 'last', 'abc'
        self.search = ''
        self.products_in_list = []  # for request if get_all_products

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
        self.current = False

    def fill_allproducts_list(self):
        self.all_products = sqlite_requests.get_all_products(USER.name, self.search, self.sort,
                                                             self.products_to_show, self.products_in_list)
        self.current_products = sqlite_requests.get_current_products(USER.name,
                                                                     self.parent_listrepresentation)
        current_products_names = [prod[0] for prod in self.current_products]
        for index in range(self.products_to_show):
            try:
                product = self.all_products[index]
            except IndexError:
                continue
            Product = AllProductRepresentation()
            Product.parent_listrepresentation = self.parent_listrepresentation
            Product.name = product[0]
            Product.units = product[1]
            Product.ids.units.text = str(Product.units)
            try:
                Product.rating = product[2]
                Product.average_rating = product[3]
                Product.frequency_of_use = product[4]
                Product.quality = product[5]
                Product.last_use = product[6]
                Product.note = product[7]
                Product.selected = (Product.name in current_products_names)
                self.products_in_list.append(Product.name)
            except IndexError:
                pass
            Product.ids.representation.text = str(Product.name)
            Product.ids.selected.active = Product.selected
            self.ids.all_products_list.add_widget(Product)

    def on_pre_open(self):
        self.sort = 'popular'
        self.search = ''
        self.product_pages_to_show = 1
        self.products_to_show = 20

        self.ids.all_products_list.clear_widgets()
        self.products_in_list.clear()
        self.fill_allproducts_list()

    def show_more_products(self):
        self.product_pages_to_show += 1

        self.fill_allproducts_list()

    def on_dismiss(self):
        self.parent_productlist.on_pre_open()

    def update_sort(self, sort_button_text=None):

        self.product_pages_to_show = 1
        self.sort = sort_button_text if sort_button_text else self.sort
        self.search = self.ids.search.text if self.ids.search.text != 'Start typing the product name' else ''

        self.ids.all_products_list.clear_widgets()
        self.products_in_list.clear()
        self.fill_allproducts_list()

    def add_product(self):
        sqlite_requests.sqlite_fill_table('personal_products', self.ids.search.text, 'шт', USER.name,
                                          0, 0, 0, 0, round(time.time()), '')
        self.ids.search.text = ''
        self.update_sort()
