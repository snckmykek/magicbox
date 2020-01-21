from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from sqlite_requests import sqlite_requests
from global_variables import LIST, USER
from contents.list.allproducts_list.allproduct_representation import AllProductRepresentation
from contents.list.product_details.main_box import ProductDetails
from kivy.uix.boxlayout import BoxLayout
import time

Builder.load_file(r'contents/list/allproducts_list/main_box.kv')

class Test(AllProductRepresentation):
    pass

class FirstBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(FirstBoxLayout, self).__init__(**kwargs)

        self.size_hint_y = None
        self.orientation = 'vertical'
        self.height = 0

        for i in range(100):
            test = Test()
            self.add_widget(test)
            self.height = self.height + test.height


class AllProductsList(ModalView):

    def __init__(self, **kwargs):
        super(AllProductsList, self).__init__(**kwargs)

        self.FBL = FirstBoxLayout()

        self.ids.all_products_list.spacing = LIST.list_representation.spacing

        self.parent_listrepresentation = ObjectProperty
        self.parent_productlist = ObjectProperty
        self.product_details = ProductDetails()

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
                                                             20, self.products_in_list)  #self.products_to_show, self.products_in_list)
        self.current_products = sqlite_requests.get_current_products(USER.name,
                                                                     self.parent_listrepresentation)
        current_products_names = [prod[0] for prod in self.current_products]
        self.FBL.height = 0
        for index in range(20):  # self.products_to_show):
            try:
                product = self.all_products[index]
            except IndexError:
                # test
                Product = self.FBL.children[index]
                Product.parent_listrepresentation = self.parent_listrepresentation
                Product.parent_allproducts = self
                Product.ids.units.text = ''
                Product.ids.representation.text = ''
                Product.ids.selected.active = False
                continue
            Product = self.FBL.children[index]  # AllProductRepresentation()
            self.FBL.height = self.FBL.height + self.FBL.children[index].height  # test
            Product.parent_listrepresentation = self.parent_listrepresentation
            Product.parent_allproducts = self
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
                Product.rating = 0
            Product.ids.representation.text = str(Product.name)
            Product.ids.selected.active = Product.selected
        self.ids.all_products_list.add_widget(self.FBL)

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

        self.products_in_list.clear()  # test
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

    def delete_product_from_list(self, product):
        self.ids.all_products_list.remove_widget(product)
