from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from global_variables import LIST


Builder.load_file(r'contents/budget/checks/budget_product_representation.kv')


class BudgetProductRepresentation(BoxLayout):

    def __init__(self, **kwargs):
        super(BudgetProductRepresentation, self).__init__(**kwargs)

        self.height = LIST.product_representation.height

