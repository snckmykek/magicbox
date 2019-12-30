from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
import global_variables
from sqlite_requests import sqlite_requests
import time
from kivy.properties import ObjectProperty

Builder.load_file(r'contents/list/elements/boxes.kv')


class ProductsListRepresentation(BoxLayout):
    """Element for List of products lists.
    """

    def __init__(self, **kwargs):
        super(ProductsListRepresentation, self).__init__(**kwargs)
        self.ProductsListBox = ProductsList()
        self.height = global_variables.LIST_REPRESENTATION_SIZE[0]

    def open_products_list(self, name_of_list):
        self.ProductsListBox.parent_listrepresentation = name_of_list
        self.ProductsListBox.open()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):  # only for selected object
            self.open_products_list(self.ids.representation.text)
        return super(ProductsListRepresentation, self).on_touch_down(touch)


class ProductsList(ModalView):

    def __init__(self, **kwargs):
        super(ProductsList, self).__init__(**kwargs)

        self.ids.addlist_but.size = global_variables.BUTTON_SIZE

        self.current_products = []
        self.parent_listrepresentation = ''
        self.AllProductsListBox = AllProductsList()

    def open_all_products_list(self):
        self.AllProductsListBox.parent_listrepresentation = self.parent_listrepresentation
        self.AllProductsListBox.parent_productlist = self
        self.AllProductsListBox.open()

    def on_pre_open(self):
        self.ids.products_list.clear_widgets()
        self.current_products = sqlite_requests.get_current_products(global_variables.USER,
                                                                     self.parent_listrepresentation)
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


class ProductRepresentation(BoxLayout):
    """Element for List of products.
    """

    def __init__(self, **kwargs):
        super(ProductRepresentation, self).__init__(**kwargs)

        self.height = global_variables.PRODUCT_REPRESENTATION_SIZE[0]
        self.parent_listrepresentation = ''
        self.parent_productlist = ObjectProperty

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
                                                 {'user': global_variables.USER, 'name': self.name,
                                                  'products_list': self.parent_listrepresentation})
            self.parent_productlist.sort_products_list()

            if self.ids.bought.active:
                self.ids.representation.strikethrough = True
                self.ids.representation.color = (.5, .5, .5, 1)
                self.ids.user.color = (.5, .5, .5, 1)
            else:
                self.ids.representation.strikethrough = False
                self.ids.representation.color = (0, 0, 0, 1)
                self.ids.user.color = (0, 0, 0, 1)

        else:
            pass


class AllProductsList(ModalView):

    def __init__(self, **kwargs):
        super(AllProductsList, self).__init__(**kwargs)

        self.parent_listrepresentation = ''
        self.parent_productlist = ObjectProperty

        self.all_products = []
        self.current_products = []
        self.product_pages_to_show = 1  # how_many_product_pages_to_show*how_many_products_to_show
        self.products_to_show = 20
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
        self.all_products = sqlite_requests.get_all_products(global_variables.USER, self.search, self.sort,
                                                             self.products_to_show, self.products_in_list)
        self.current_products = sqlite_requests.get_current_products(global_variables.USER,
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
        self.sort = sort_button_text if (sort_button_text is not None) else self.sort
        self.search = self.ids.search.text if self.ids.search.text != 'Start typing the product name' else ''

        self.ids.all_products_list.clear_widgets()
        self.products_in_list.clear()
        self.fill_allproducts_list()

    def hello(self) -> object:
        print(1)


class AllProductRepresentation(BoxLayout):
    """Element for List of all products.
    """

    def __init__(self, **kwargs):
        super(AllProductRepresentation, self).__init__(**kwargs)

        self.height = global_variables.PRODUCT_REPRESENTATION_SIZE[0]

        self.parent_listrepresentation = ''

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

        if sqlite_requests.is_product_in_table('current_products', global_variables.USER,
                                               self.name, self.parent_listrepresentation) is self.selected:
            return  # If called by creating of Product in on_pre_open of AllProductsList

        if sqlite_requests.is_product_in_table('personal_products', global_variables.USER, self.name):
            sqlite_requests.sqlite_update_record('personal_products',
                                                 {
                                                     'frequency_of_use': self.frequency_of_use,
                                                     'last_use': self.last_use
                                                 },
                                                 {'user': global_variables.USER, 'name': self.name})
        else:
            sqlite_requests.sqlite_fill_table('personal_products', self.name, self.units, user=global_variables.USER,
                                              frequency_of_use=1, last_use=round(time.time()))

        if self.selected:
            sqlite_requests.sqlite_fill_table('current_products', self.name, self.units, user=global_variables.USER,
                                              products_list=self.parent_listrepresentation, price=self.current_price,
                                              quantity=self.quantity, bought='False')
        else:
            sqlite_requests.sqlite_delete_record('current_products', name=self.name, user=global_variables.USER,
                                                 products_list=self.parent_listrepresentation)


class AddProduct(ModalView):

    def __init__(self, **kwargs):
        super(AddProduct, self).__init__(**kwargs)

        self.ids.add_but.height = global_variables.BUTTON_SIZE[0]

        self.current_products = []
        self.parent_listrepresentation = ''
        self.AllProductsListBox = AllProductsList()

    def open_all_products_list(self):
        self.AllProductsListBox.parent_listrepresentation = self.parent_listrepresentation
        self.AllProductsListBox.parent_productlist = self
        self.AllProductsListBox.open()

    def on_pre_open(self):
        self.ids.products_list.clear_widgets()
        self.current_products = sqlite_requests.get_current_products(global_variables.USER,
                                                                     self.parent_listrepresentation)
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