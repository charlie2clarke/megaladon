import datetime
from random import randint
from .data_access import DataAccess

class Query:
    def __init__(self):
        self.data_access = DataAccess()

    def add_order(self, item, first_name, last_name, line_one, line_two, city):
        
        def get_product_id(item):
            queryset = self.data_access.execute('''
                SELECT
                    Product.id
                FROM
                    Product
                WHERE
                    Product.product_name=?
            ''', (item,))
            return queryset.fetchone()
        
        customer = self.data_access.execute('''
            INSERT INTO Customer(first_name, last_name)
            VALUES(?, ?)
        ''', (first_name, last_name))
        
        address = self.data_access.execute('''
            INSERT INTO Address(line_one, line_two, city)
            VALUES(?, ?, ?)
        ''', (line_one, line_two, city))

        last_customer = customer.lastrowid
        last_address = address.lastrowid

        self.data_access.execute('''
            INSERT INTO Customer_Address(customer_id, address_id)
            VALUES(?, ?)
        ''', (last_customer, last_address))

        random_postage = randint(1, 2)
        date_now = str(datetime.datetime.strptime('01/08/2015', '%d/%m/%Y').date())

        purchase = self.data_access.execute('''
            INSERT INTO Purchase(platform_id, customer_id, status_id, postage_id, created_date)
            VALUES(?, ?, ?, ?, ?)
        ''', (1, last_customer, 1, random_postage, date_now))

        product_id = get_product_id(item)[0]

        self.data_access.execute('''
            INSERT INTO Purchase_Product(purchase_id, product_id, quantity)
            VALUES(?, ?, ?)
        ''', (purchase.lastrowid, product_id, 1))

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
                Purchase.id
        ''', None)
        return queryset.fetchall()