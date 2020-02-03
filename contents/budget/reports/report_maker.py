from kivy.lang import Builder
from kivy.uix.modalview import ModalView

import pandas as pd
import sqlite3

Builder.load_file(r'contents/budget/reports/report_maker.kv')


class ReportMaker(ModalView):

    def __init__(self, **kwargs):
        super(ReportMaker, self).__init__(**kwargs)

    def get_report(self):
        lst = get_report()
        shop = lst[0]
        prod = lst[1]
        self.ids.report.text = str(shop) + '\n' + str(prod)


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect('database_havka.db')
        self.cur = self.con.cursor()

    def read_table(self, table_name, columns=None, sort_by=None, values=None, products=[], **wheres):
        request = 'SELECT '
        if columns:
            for column in columns:
                request += column + ', '
            request = request[:-2]
        else:
            request += '*'
        request += ' FROM ' + table_name
        if wheres or products:
            request += ' WHERE '
            if wheres:
                request += '"'
                for col, val in wheres.items():
                    request += col + '" = "' + str(val) + '" AND "'
                if products:
                    request = request[:-1]
                else:
                    request = request[:-6]
            if products:
                request += 'name IN ('
                for prod in products:
                    request += '"{}", '.format(prod)
                request = request[:-2] + ')'

        if sort_by:
            request += ' ORDER BY ' + sort_by

        df = pd.read_sql_query(request, self.con)

        return df

    def close(self):
        self.cur.close()
        self.con.close()


db = Database()


def get_report():
    df = db.read_table('budget_products')

    categories = db.read_table('personal_products', products=list(df['name']), is_category=False,
                               columns=['name', 'category'])

    new_table = pd.merge(df, categories)

    grouped_shop_price = new_table.groupby(['date', 'shop_name'])['price'].sum()
    grouped_prod = new_table.groupby(['category'])['quantity', 'price'].sum()

    return [grouped_shop_price, grouped_prod]
