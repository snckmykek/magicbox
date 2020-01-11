from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from sqlite_requests import sqlite_requests
from global_variables import LIST, USER

Builder.load_file(r'contents/list/product_details/main_box.kv')


class ProductDetails(ModalView):

    def __init__(self, **kwargs):
        super(ProductDetails, self).__init__(**kwargs)

        self.parent_product = ObjectProperty

    def on_pre_open(self):
        self.ids.name.text = self.parent_product.name
        self.ids.units.text = self.parent_product.units
        self.ids.rating.text = str(self.parent_product.rating)
        self.ids.quality.text = str(self.parent_product.quality)
        self.ids.current_price.text = str(self.parent_product.current_price)
        self.ids.note.text = self.parent_product.note

    def delete_product(self):
        self.parent_product.delete_product()
        self.dismiss()

    def save_changes(self):
        if sqlite_requests.is_product_in_table('personal_products', USER.name, self.parent_product.name):
            sqlite_requests.sqlite_update_record('personal_products',
                                                 {'name': self.ids.name.text,
                                                  'units': self.ids.units.text,
                                                  'rating': self.ids.rating.text,
                                                  'quality': self.ids.quality.text,
                                                  'note': self.ids.note.text
                                                  },
                                                 {'name': self.parent_product.name,
                                                  'user': USER.name
                                                  })
        else:
            sqlite_requests.sqlite_fill_table('personal_products',
                                              self.parent_product.name,
                                              'шт',
                                              USER.name,
                                              self.parent_product.rating,
                                              0,
                                              0,
                                              self.parent_product.quality,
                                              0,
                                              self.parent_product.note)
        self.parent_product.parent_allproducts.on_pre_open()
        self.dismiss()
