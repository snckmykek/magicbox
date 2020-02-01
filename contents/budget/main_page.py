from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from contents.budget.checks.new_check_adder import CheckAdder

Builder.load_file(r'contents/budget/main_page.kv')


class Budget(BoxLayout):

    def __init__(self, **kwargs):
        super(Budget, self).__init__(**kwargs)

        self.check_adder = CheckAdder()

    def add_new_check(self):
        self.check_adder.open()


BudgetBox = Budget()
