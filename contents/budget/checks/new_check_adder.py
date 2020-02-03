from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.button import Button
from contents.budget.checks.budget_product_representation import BudgetProductRepresentation
import json
from sqlite_requests import sqlite_requests
from global_variables import USER
from kivy.uix.popup import Popup

import time

try:
    from android.permissions import request_permissions, Permission
except:
    pass

Builder.load_file(r'contents/budget/checks/new_check_adder.kv')


class CheckAdder(ModalView):

    def __init__(self, **kwargs):
        super(CheckAdder, self).__init__(**kwargs)

        self.category_adder = CategoryAdder()

        self.date = ''
        self.shop_name = ''
        self.shop_address = ''
        self.sum = ''
        self.products = []

        self.data_list = []

    def next_check(self):
        try:
            data = json.loads(self.data_list[0])
        except:
            return False

        self.date = data['date']
        self.shop_name = data['shopName']
        self.shop_address = data['shopAddress']
        self.sum = data['totalSum']

        self.ids.date.text = str(self.date)
        self.ids.shop_name.text = str(self.shop_name)
        # self.ids.shop_address.text = str(shop_address)
        self.ids.sum.text = str(self.sum)
        self.products = data['products']

        self.data_list.remove(self.data_list[0])

        self.ids.products_in_check.clear_widgets()
        for prod in self.products:
            PR = BudgetProductRepresentation()
            PR.ids.name.text = prod['name']
            PR.ids.quantity.text = str(prod['quantity'])
            PR.ids.price.text = str(prod['price'])
            PR.ids.sum.text = str(prod['quantity'] * prod['price'])

            self.ids.products_in_check.add_widget(PR)

        return True

    def go(self):
        try:
            # with open(self.ids.file.text, 'r', encoding='utf-8') as read_json:
            #     data = json.load(read_json)
            self.data_list = self.ids.file.text.split('\n')
        except:
            return

        self.next_check()

    def choose_file(self):
        LD = LoadDialog()
        try:
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                                 Permission.READ_EXTERNAL_STORAGE])
            LD.ids.filechooser.path = '/data/data/org.test.myapp'
        except:
            pass
        LD.button = self.ids.file
        LD.open()

    def add_this_check(self):

        products_names = [prod['name'] for prod in self.products]

        self.category_adder.parent_check = self
        new_products = sqlite_requests.get_products_not_in_table('personal_products', USER.name, products_names)
        self.category_adder.new_products = new_products

        if new_products:
            self.category_adder.open()
        else:
            self.update_bd_and_try_next_check()

    def update_bd_and_try_next_check(self):
        self.update_bd()

        if not self.next_check():
            self.dismiss()

    def update_bd(self):
        # Нужно сделать проверку на дубли по чеку, а тут оптимизивать вставку в БД, а не ебенить в цикле
        # Пока вместо проверок и тд тупо удаляются данные по чеку и перезаписываются
        sqlite_requests.sqlite_delete_record('budget_products', date=self.date, shop_name=self.shop_name)

        for prod in self.products:
            sqlite_requests.fill_budget_products_table(self.date, self.shop_name, self.shop_address, prod['name'],
                                                       prod['quantity'], prod['price'])


class CategoryAdder(ModalView):

    def __init__(self, **kwargs):
        super(CategoryAdder, self).__init__(**kwargs)

        self.parent_check = ''
        self.new_products = []
        self.current_product = ''

    def search(self):

        categories = sqlite_requests.get_all_products(USER.name, search=self.ids.search.text)

        self.ids.categories.clear_widgets()
        for category in categories:
            button = Button(text=category[0])
            button.bind(on_press=self.add_product)
            self.ids.categories.add_widget(button)
        for cat in self.ids.categories.children:
            cat.text_size = cat.size

    def add_product(self, instance):
        sqlite_requests.sqlite_fill_table('personal_products', self.current_product, user=USER.name,
                                          category=instance.text)
        self.new_products.remove(self.current_product)
        self.on_pre_open()  # Не нравится на пре опен ссылаться, мб вынести в еще одну функцию? Хотя тогда
        # нагромождение функций

    def on_pre_open(self):
        if self.new_products:
            self.current_product = self.new_products[0]
            self.ids.label.text = self.current_product
        else:
            self.close()

    def close(self):
        self.parent_check.update_bd_and_try_next_check()
        self.dismiss()

    def add_category(self):
        sqlite_requests.sqlite_fill_table('personal_products',
                                          self.ids.search.text[0].upper() + self.ids.search.text[1:], 'шт', USER.name,
                                          0, 0, 0, 0, round(time.time()), '', is_category=True)
        self.search()


class LoadDialog(Popup):

    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)

        self.button = ''

    def load(self, path, selection):
        try:
            self.button.text = selection[0].replace('\\', '/').replace('//', '/')
        except:
            self.button.text = selection[0]
        self.dismiss()
