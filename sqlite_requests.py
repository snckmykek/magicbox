# coding=utf-8
# хз зачем надпись выше лол, но пока оставлю
import sqlite3
import http_requests
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
        self.sqlite_create_db()
        self.fill_db_global_products()

    def close(self):
        self.cur.close()
        self.con.close()

    def sqlite_create_db(self):

        self.cur.execute('CREATE TABLE IF NOT EXISTS global_products('
                         'name TEXT,'  # Name of product 
                         'category TEXT,'  
                         'units TEXT,'
                         'upper_name TEXT)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS personal_products('  # Products of current user
                         'user TEXT,'
                         'name TEXT,'  # Name of product
                         'is_category BOOLEAN,'  
                         'category TEXT,'  
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
        self.cur.execute('CREATE TABLE IF NOT EXISTS lists('  
                         'user TEXT,'
                         'name TEXT,'
                         'upper_name TEXT)')

        # Мб ебануть в другую БД? Шобэ не перегружалась эта. Хотя если хранить только чеки за месяц, а остальные,
        # в облаке, то похуй наверн. Протестить в далёком, светлом будущем
        self.cur.execute('CREATE TABLE IF NOT EXISTS budget_products('
                         'date TEXT,'
                         'shop_name TEXT,'
                         'shop_address TEXT,'
                         'name TEXT,'
                         'quantity FLOAT,'
                         'price FLOAT,'
                         'upper_shop_name TEXT,'
                         'upper_product_name TEXT)')

    def fill_budget_products_table(self, date, shop_name, shop_address, product_name, quantity, price):
        self.cur.execute('INSERT INTO budget_products VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}",'
                         '"{7}")'.format(date, shop_name, shop_address, product_name,
                                         quantity, price, shop_name.upper(), product_name.upper()))
        self.con.commit()

    def sqlite_fill_table(self, table_name, name, units='шт', user='noname', rating=0.0, average_rating=0.0,
                          frequency_of_use=0, quality=0.0, last_use=0, note='', price=0.00, quantity=0.000,
                          products_list='noname', bought=False, category='', is_category=False):

        if table_name == 'global_products':
            self.cur.execute('INSERT INTO global_products VALUES("{0}","{1}","{2}","{3}")'.format(name, category , units, name.upper()))
        elif table_name == 'personal_products':
            self.cur.execute('INSERT INTO personal_products VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}",'
                             '"{7}","{8}","{9}","{10}","{11}")'.format(user, name, is_category, category, units,
                                    rating, average_rating, frequency_of_use, quality, last_use, note, name.upper()))
        elif table_name == 'current_products':
            self.cur.execute('INSERT INTO current_products VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}")'
                             .format(user, products_list, name, units, price, quantity, bought, name.upper()))
        elif table_name == 'lists':
            self.cur.execute('INSERT INTO lists VALUES("{0}","{1}","{2}")'.format(user, name, name.upper()))
        self.con.commit()

    def sqlite_read_table(self, table_name, columns=None, sort_by=None, values=None):
        request = 'SELECT '
        if columns:
            for column in columns:
                request += column + ', '
            request = request[:-2]
        else:
            request += '*'
        request += ' FROM ' + table_name
        if sort_by:
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

    def get_all_products(self, user, search='', sort='popular', products_to_show=10, products_in_list=[],
                         only_categories=True):

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

        if only_categories:
            request += ' AND is_category = "True"'

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

    def get_products_not_in_table(self, table_name, user, products_names, products_list=None):
        """return list of objects not in the list"""
        request = 'SELECT name FROM {0} WHERE "user" = "{1}"'.format(table_name, user)
        request += ' AND name IN ('
        for prod in products_names:
            request += '"{}", '.format(prod)
        request = request[:-2] + ')'
        if products_list is not None:
            request += ' AND "products_list" = "{}"'.format(products_list)
        self.cur.execute(request)

        products_names_in_table = [prod[0] for prod in self.cur.fetchall()]

        return list(set(products_names) - set(products_names_in_table))

    def get_the_number_of_records_in_the_table(self, table='global_products'):
        request = 'SELECT COUNT(*) FROM {}'.format(table)
        self.cur.execute(request)
        return self.cur.fetchall()[0][0]

    def fill_db_global_products(self):

        if self.get_the_number_of_records_in_the_table('global_products') == 0:
            for prod in http_requests.get_global_products():
                self.sqlite_fill_table('global_products', prod, 'шт')


sqlite_requests = Database()


