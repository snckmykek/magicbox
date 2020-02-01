import json
from sqlite_requests import sqlite_requests
from global_variables import USER


with open('13.json', 'r', encoding='utf-8') as read_json:
    data = json.load(read_json)

print(data)

date = data['date']
shop_name = data['shopName']
shop_address = data['shopAddress']
sum = data['totalSum']
products = data['products']

products_names = [prod['name'] for prod in products]

new_products = sqlite_requests.get_products_not_in_table('personal_products', USER.name, products_names)

for prod in new_products:

    sqlite_requests.sqlite_fill_table('personal_products', prod, user=USER.name, category=1)
    a = sqlite_requests.get_all_products(USER.name, search='', only_categories=True)

print(new_products)
# for prod in products:
#     sqlite_requests.