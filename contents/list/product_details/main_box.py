from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from sqlite_requests import sqlite_requests
from global_variables import LIST, USER

Builder.load_file(r'contents/list/product_details/main_box.kv')


class ProductDetails(ModalView):

    def __init__(self, **kwargs):
        super(ProductDetails, self).__init__(**kwargs)
