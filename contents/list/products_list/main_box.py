from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from contents.list.allproducts_list.main_box import AllProductsList
from contents.list.products_list.product_representation import ProductRepresentation
from global_variables import USER
from sqlite_requests import sqlite_requests

Builder.load_file(r'contents/list/products_list/main_box.kv')


class ProductsList(ModalView):

    def __init__(self, **kwargs):
        super(ProductsList, self).__init__(**kwargs)

        self.current_products = []
        self.parent_listrepresentation = ''
        self.AllProductsListBox = AllProductsList()

    def open_all_products_list(self):
        self.AllProductsListBox.parent_listrepresentation = self.parent_listrepresentation
        self.AllProductsListBox.parent_productlist = self
        self.AllProductsListBox.open()

    def on_pre_open(self):
        self.ids.products_list.clear_widgets()
        self.current_products = sqlite_requests.get_current_products(USER.name, self.parent_listrepresentation)
        self.current_products.sort(key=lambda i: i[4])
        for product in self.current_products:
            Product = ProductRepresentation()
            Product.parent_listrepresentation = self.parent_listrepresentation
            Product.parent_productlist = self
            Product.name = product[0]
            Product.units = product[1]
            try:
                Product.price = product[2]
                Product.quantity = product[3]
                Product.bought = (product[4] == 'True')
            except IndexError:
                pass
            Product.ids.representation.text = str(Product.name)
            Product.ids.bought.active = Product.bought
            self.ids.products_list.add_widget(Product)

    def sort_products_list(self):
        children_array = self.ids.products_list.children.copy()
        self.ids.products_list.clear_widgets()
        children_dict = {}
        for elem in children_array:
            children_dict.update({elem: [elem.bought, elem.name]})
        children_dict = sorted(children_dict.items(), key=lambda item: (item[1][0], item[1][1]))
        for elem in children_dict:
            self.ids.products_list.add_widget(elem[0])

    def delete_product_from_list(self, product):
        self.ids.products_list.remove_widget(product)
