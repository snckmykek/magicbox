# coding=utf-8
import sqlite3
import time


class Database(object):
    """
    sqlite_create_db # Create db and tables If not exists
    sqlite_fill_table(table_name, etc.) # Fill table
    sqlite_read_table(table_name, etc.) # Read table
    sqlite_delete_record(table_name, etc.) # Delete record in table
    sqlite_update_record(table_name, etc.) # Change record in table
    get_list_of_columns_without_useless(table_name, *useless) # return columns of table without useless columns
    fill_all_products(user) # return all_products consisting of all global products and personal products of user
    fill_current_products(user) # return products of current user from table current_products
    """

    def __init__(self):
        self.con = sqlite3.connect('database_havka.db')
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()

    def sqlite_create_db(self):

        self.cur.execute('CREATE TABLE IF NOT EXISTS global_products('
                         'name TEXT,'  # Name of product
                         'units TEXT,'
                         'upper_name TEXT)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS personal_products('  # Products of current user
                         'user TEXT,'
                         'name TEXT,'  # Name of product
                         'units TEXT,'
                         'rating FLOAT,'
                         'average_rating FLOAT,'
                         'frequency_of_use INTEGER,'
                         'quality INTEGER,'
                         'last_use INTEGER,'  # Date+time in Unix
                         'note TEXT,'
                         'upper_name TEXT)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS current_products('  # In List of products now
                         'user TEXT,'
                         'products_list TEXT,'
                         'name TEXT,'  # Name of product
                         'units TEXT,'
                         'price FLOAT,'
                         'quantity FLOAT,'
                         'bought BOOLEAN,'  # List of products
                         'upper_name TEXT)')

    def sqlite_fill_table(self, table_name, name, units, user='noname', rating=0.0, average_rating=0.0,
                          frequency_of_use=0, quality=0.0, last_use=0, note='', price=0.00, quantity=0.000,
                          products_list='noname', bought=False):

        if table_name == 'global_products':
            self.cur.execute('INSERT INTO global_products VALUES("{0}","{1}","{2}")'.format(name, units, name.upper()))
        elif table_name == 'personal_products':
            self.cur.execute('INSERT INTO personal_products VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}",'
                             '"{7}","{8}","{9}")'.format(user, name, units, rating, average_rating,
                                                         frequency_of_use, quality, last_use, note, name.upper()))
        elif table_name == 'current_products':
            self.cur.execute('INSERT INTO current_products VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}")'
                             .format(user, products_list, name, units, price, quantity, bought, name.upper()))
        self.con.commit()

    def sqlite_read_table(self, table_name, columns=None, sort_by=None, values=None):
        request = 'SELECT '
        if columns is None:
            request += '*'
        else:
            for column in columns:
                request += column + ', '
            request = request[:-2]
        request += ' FROM ' + table_name
        if sort_by is not None:
            request += ' ORDER BY ' + sort_by

        self.cur.execute(request)
        data = self.cur.fetchall()

        return data

    def sqlite_delete_record(self, table_name, **params):
        # params = {col1: val1, col2: val2}
        request = 'DELETE FROM ' + table_name + ' WHERE "'
        for col, val in params.items():
            request += col + '" = "' + val + '" AND "'
        request = request[:-6]  # Cutting last ' AND '
        self.cur.execute(request)
        self.con.commit()

    def sqlite_update_record(self, table_name, params, where):
        # where = {col1: val1, col2: val2}
        # params = {col1: val1, col2: val2}
        request = 'UPDATE ' + table_name + ' SET "'
        for col, val_new in params.items():
            request += col + '" = "' + str(val_new) + '", "'
        request = request[:-3]  # Cutting last ', "'
        request += ' WHERE "'
        for col, val in where.items():
            request += col + '" = "' + str(val) + '" AND "'
        request = request[:-6]  # Cutting last ' AND '
        self.cur.execute(request)
        self.con.commit()

    def get_list_of_columns_without_useless(self, table_name, *useless):
        self.cur.execute('pragma table_info("{}")'.format(table_name))
        cols = [col[1] for col in self.cur.fetchall()]
        return [col for col in cols if col not in useless]

    def get_all_products(self, user, search='', sort='popular', products_to_show=20, products_in_list=None):

        # for personal products
        cols = self.get_list_of_columns_without_useless('personal_products', 'user')
        cols = ', '.join(cols)
        if search:
            request = 'SELECT {} FROM personal_products WHERE user = "{}" AND upper_name LIKE "%{}%"'.format(cols, user,
                                                                                                    search.upper())
        else:
            request = 'SELECT {} FROM personal_products WHERE user = "{}"'.format(cols, user)

        if products_in_list:
            request += ' AND name NOT IN ('
            for prod in products_in_list:
                request += '"{}", '.format(prod)
            request = request[:-2] + ')'

        if sort == 'popular':
            request += ' ORDER BY frequency_of_use DESC'
        elif sort == 'last':
            request += ' ORDER BY last_use DESC'
        elif sort == 'abc':
            request += ' ORDER BY name ASC'

        request += ' LIMIT "{}"'.format(products_to_show)
        self.cur.execute(request)
        personal_products = self.cur.fetchall()
        personal_product_names = [prod[0] for prod in personal_products]

        # for global products
        if search:
            request = 'SELECT * FROM global_products WHERE upper_name LIKE "%{}%"'.format(search.upper())
        else:
            request = 'SELECT * FROM global_products'

        product_names = personal_product_names + products_in_list
        if product_names:
            if search:
                request += ' AND'
            else:
                request += ' WHERE'
            request += ' name NOT IN ('
            for prod in product_names:
                request += '"{}", '.format(prod)
            request = request[:-2] + ')'
        request += ' LIMIT "{}"'.format(products_to_show - len(personal_products))
        self.cur.execute(request)
        global_products = self.cur.fetchall()

        all_products = personal_products + global_products

        return all_products

    def get_current_products(self, user, products_list):
        cols = self.get_list_of_columns_without_useless('current_products', 'user', 'products_list')
        cols = ', '.join(cols)
        self.cur.execute('SELECT {0} FROM current_products WHERE user = "{1}" AND products_list = "{2}"'
                         .format(cols, user, products_list))
        current_products = self.cur.fetchall()

        return current_products

    def is_product_in_table(self, table_name, user, products_name, products_list=None):
        """return bool"""
        request = 'SELECT * FROM {0} WHERE "user" = "{1}" AND "name" = "{2}"'.format(table_name, user, products_name)
        if products_list is not None:
            request += ' AND "products_list" = "{}"'.format(products_list)
        self.cur.execute(request)
        if self.cur.fetchall():
            return True
        else:
            return False


sqlite_requests = Database()


def remake_db():
    sqlite_requests.sqlite_create_db()
    for i in range(30):
        sqlite_requests.sqlite_fill_table('global_products', 'Какой-то продукт ' + str(i), 'кг')

    for i in range(30):
        sqlite_requests.sqlite_fill_table('global_products', 'Общий продукт ' + str(i), 'кг')

    for i in range(10):
        sqlite_requests.sqlite_fill_table('personal_products', 'Личный продукт ' + str(i), 'шт', 'Admin', 3, 5, 123, 4,
                                          0, 'test ' + str(i))

    for i in range(10, 20):
        sqlite_requests.sqlite_fill_table('personal_products', 'Личный продукт ' + str(i), 'кг', 'Admin')

    for i in range(30, 50):
        sqlite_requests.sqlite_fill_table('global_products', 'Общий продукт ' + str(i), 'шт')

    for i in range(10):
        sqlite_requests.sqlite_fill_table('personal_products', 'Какой-то продукт ' + str(i), 'шт', 'Admin 2')

    for i in range(110, 120):
        sqlite_requests.sqlite_fill_table('personal_products', 'Личный продукт ' + str(i), 'кг', 'Admin 2')


# remake_db()
