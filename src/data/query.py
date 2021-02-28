from datetime import datetime
from random import randint
from .data_access import DataAccess


class Query:
    def __init__(self):
        self.data_access = DataAccess()

    def add_order(self, items_and_quantity, first_name, last_name, line_one, line_two, city):

        def get_product_id(item_and_quantity):
            # Replacing item name with id
            queryset = self.data_access.execute('''
                SELECT
                    Product.id
                FROM
                    Product
                WHERE
                    Product.product_name=?
            ''', (item_and_quantity['item'],))
            item_id = queryset.fetchone()
            item_id = item_id[0]
            item_and_quantity['item'] = item_id

            return item_and_quantity

        def check_if_customer_exists():
            # Duck typing - if it looks like a duck, quacks like a duck, then its probably a duck...
            queryset = self.data_access.execute('''
                SELECT
                    * 
                FROM
                    Customer_Address
                INNER JOIN Customer ON Customer.id = Customer_Address.customer_id
                INNER JOIN Address ON Address.id = Customer_Address.address_id
                WHERE
                    Customer.first_name=? AND Customer.last_name=? AND Address.line_one=? AND Address.city=?
            ''', (first_name, last_name, line_one, city))

            return queryset.fetchone()

        existing_customer = check_if_customer_exists()

        if existing_customer is None:
            customer = self.data_access.execute('''
                INSERT INTO Customer(first_name, last_name)
                VALUES(?, ?)
            ''', (first_name, last_name))

            address = self.data_access.execute('''
                INSERT INTO Address(line_one, line_two, city)
                VALUES(?, ?, ?)
            ''', (line_one, line_two, city))

            customer_id, address_id = customer.lastrowid, address.lastrowid

            self.data_access.execute('''
                INSERT INTO Customer_Address(customer_id, address_id)
                VALUES(?, ?)
            ''', (customer_id, address_id))
        else:
            customer_id, address_id = existing_customer[0], existing_customer[1]

        random_postage = randint(1, 2)
        date_now = datetime.today().strftime('%Y-%m-%d')

        # Sometimes unique constraint fails because it is possible that the previous order in 
        # the database is for the same customer which would make the row about to be added a duplicate

        purchase = self.data_access.execute('''
            INSERT INTO Purchase(platform_id, customer_id, status_id, postage_id, created_date)
            VALUES(?, ?, ?, ?, ?)
        ''', (1, customer_id, 1, random_postage, date_now))

        items_and_quantity = [get_product_id(
            product) for product in items_and_quantity]

        for item in items_and_quantity:
            self.data_access.execute('''
                INSERT INTO Purchase_Product(purchase_id, product_id, quantity)
                VALUES(?, ?, ?)
            ''', (purchase.lastrowid, item['item'], item['quantity']))

    def get_all_data(self):
        queryset = self.data_access.execute('''
            SELECT
                Purchase_Product.purchase_id,
                Product.product_name,
                Purchase_Product.quantity,
                Customer.first_name,
                Customer.last_name,
                Customer.email,
                Address.line_one,
                Address.line_two,
                Address.city,
                Address.postcode,
                Status.status_description,
                Purchase.created_date,
                Purchase.dispatched_date,
                Purchase.completed_date,
                Postage.postage_description,
                Product.individual_price,
                Product.id,
                Product.aisle,
                Product.shelf
            FROM
                Product
                INNER JOIN Purchase_Product ON Purchase_Product.product_id = Product.id
                INNER JOIN Purchase ON Purchase.id = Purchase_Product.purchase_id
                INNER JOIN Status ON Status.id = Purchase.status_id
                INNER JOIN Postage ON Postage.id = Purchase.postage_id
                INNER JOIN Customer ON Customer.id = Purchase.customer_id
                INNER JOIN Customer_Address ON Customer_Address.customer_id = Customer.id
                INNER JOIN Address ON Address.id = Customer_Address.address_id
            ORDER BY
                Status.id
        ''', None)
        return queryset.fetchall()
