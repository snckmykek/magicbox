"""
This module is used for synchronization with site/server

Needs a lot of refinement.
"""


def get_global_products():
    """
    Return "global" products (common products, like Apple, Beer, Meat, etc.).

    P.S.For now don't using requests to server, server does not exist =) Now it's stub.
    """

    f = open('global_products.txt', encoding='utf-8')
    global_products = f.read().split(",")

    return global_products
