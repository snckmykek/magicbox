from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from contents.budget.checks.new_check_adder import CheckAdder
from contents.budget.reports.report_maker import ReportMaker

Builder.load_file(r'contents/budget/main_page.kv')


class Budget(BoxLayout):

    def __init__(self, **kwargs):
        super(Budget, self).__init__(**kwargs)

        self.check_adder = CheckAdder()
        self.report_maker = ReportMaker()

    def add_new_check(self):
        self.check_adder.open()

    def get_report(self):
        self.report_maker.open()


BudgetBox = Budget()
