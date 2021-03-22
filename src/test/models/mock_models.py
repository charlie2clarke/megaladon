class Address:
    def __init__(self, line_one, city):
        self.line_one = line_one
        self.city = city


class Customer:
    def __init__(self, address, first_name, last_name, email):
        self.address = address
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class Product:
    def __init__(self, product_id, product_name, price, aisle, shelf):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.aisle = aisle
        self.shelf = shelf


class Order:
    def __init__(self, order_id, customer, products, created_date, status):
        self.order_id = order_id
        self.customer = customer
        self.products = products
        self.created_date = created_date
        self.dispatched_date = "Date Now"
        self.completed_date = None
        self.status = status
