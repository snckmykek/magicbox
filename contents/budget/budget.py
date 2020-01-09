from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


class Budget(BoxLayout):
    Builder.load_file(r'contents/budget/budget.kv')


BudgetBox = Budget()
