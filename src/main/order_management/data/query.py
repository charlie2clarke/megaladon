'''Performs querys to OnlineStore database.

Is the only module executing queries - increasing cohesion
meaning that if there was a change of database it could happen
much easier.
'''
from datetime import datetime
from random import randint
from .data_access import DataAccess


class Query:
    '''Class used for exeucting SQL queries to database.'''

    def __init__(self):
        '''Inits Query.'''
        self._data_access = DataAccess()
        self._new_order_pointer = 0

    def add_order(self,
                  items_and_quantity,
                  first_name,
                  last_name,
                  line_one,
                  line_two,
                  city,
                  email,
                  index
                  ):
        '''Takes data for a single order and inserts it into the database.

        Has to implement a small amount of logic to check if order is for a new
        customer to ensure data is only stored once.

        Args:
            items_and_quantity: an array of dictionaries with key for item and
                                quantity in each.
            first_name: string of customer's first name.
            last_name: string of customer's last name.
            line_one: string of first line to customer's address.
            line_two: string of second line to customer's address.
            city: string of customer's city of residence.
            email: string of customer's email address.
            index: integer of iteration method is invoked - is used to
                   determine position at which new data should be pulled
                   from to not retrieve all data every time.
        '''

        def get_product_id(item_and_quantity):
            # Replacing item name in item_and_quantity dictionary with item id.
            queryset = self._data_access.execute('''
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
            # Duck typing - if it looks like a duck, quacks like a duck,
            # then its probably a duck...
            queryset = self._data_access.execute('''
                SELECT
                    *
                FROM
                    Customer_Address
                INNER JOIN Customer ON Customer.id =
                    Customer_Address.customer_id
                INNER JOIN Address ON Address.id =
                    Customer_Address.address_id
                WHERE
                    Customer.first_name=? AND Customer.last_name=? AND
                        Address.line_one=? AND Address.city=?
            ''', (first_name, last_name, line_one, city))

            return queryset.fetchone()

        existing_customer = check_if_customer_exists()

        if existing_customer is None:
            # New customer to enter into database.
            customer = self._data_access.execute('''
                INSERT INTO Customer(first_name, last_name, email)
                VALUES(?, ?, ?)
            ''', (first_name, last_name, email))

            address = self._data_access.execute('''
                INSERT INTO Address(line_one, line_two, city)
                VALUES(?, ?, ?)
            ''', (line_one, line_two, city))

            customer_id, address_id = customer.lastrowid, address.lastrowid

            self._data_access.execute('''
                INSERT INTO Customer_Address(customer_id, address_id)
                VALUES(?, ?)
            ''', (customer_id, address_id))
        else:
            customer_id, address_id = \
                existing_customer[0], existing_customer[1]

        # Randomly choosing postage as this isn't retrieved from Webay API.
        random_postage = randint(1, 2)
        date_now = datetime.today().strftime('%Y-%m-%d')

        purchase = self._data_access.execute('''
            INSERT INTO Purchase(
                                 platform_id,
                                 customer_id,
                                 status_id,
                                 postage_id,
                                 created_date
                                 )
            VALUES(?, ?, ?, ?, ?)
        ''', (1, customer_id, 1, random_postage, date_now))

        # If called in the first iteration this means that the row number
        # can be retrived to determine where in database new orders should
        # be looked for and not fecth all each time.
        if index == 1:
            self._set_new_order_pointer()

        items_and_quantity = [get_product_id(
            product) for product in items_and_quantity]

        last_purchase = purchase.lastrowid

        for item in items_and_quantity:
            self._data_access.execute('''
                INSERT INTO Purchase_Product(purchase_id, product_id, quantity)
                VALUES(?, ?, ?)
            ''', (last_purchase, item['item'], item['quantity']))

    def _set_new_order_pointer(self):
        # Sets integer of row number to look for new orders.
        queryset = self._data_access.execute('''
            SELECT
                MAX(id)
            FROM
                Purchase
        ''', None).fetchone()
        self._new_order_pointer = int(queryset[0])

    def get_all_data(self):
        '''Retrieves all data from database need to initialise Order.

        Only called once on startup of app.

        Returns:
            An array with a nested array for each row retrieved. Index
            of item corresponds to position selected below.
        '''
        queryset = self._data_access.execute('''
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
                INNER JOIN Purchase_Product ON Purchase_Product.product_id =
                    Product.id
                INNER JOIN Purchase ON Purchase.id =
                    Purchase_Product.purchase_id
                INNER JOIN Status ON Status.id = Purchase.status_id
                INNER JOIN Postage ON Postage.id = Purchase.postage_id
                INNER JOIN Customer ON Customer.id = Purchase.customer_id
                INNER JOIN Customer_Address ON Customer_Address.customer_id =
                    Customer.id
                INNER JOIN Address ON Address.id = Customer_Address.address_id
            ORDER BY
                Status.id
        ''', None)
        return queryset.fetchall()

    def get_new_data(self):
        '''Retrieves all rows in database for orders that haven't been
        initialised.

        Same as the above but includes a WHERE clause to only get newest
        orders.

        Has been implemented as a different method to be explicit.

        Returns:
            An array with a nested array for each row retrieved. Index
            of item corresponds to position selected below.
        '''
        queryset = self._data_access.execute('''
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
                INNER JOIN Purchase_Product ON Purchase_Product.product_id =
                    Product.id
                INNER JOIN Purchase ON Purchase.id =
                    Purchase_Product.purchase_id
                INNER JOIN Status ON Status.id = Purchase.status_id
                INNER JOIN Postage ON Postage.id = Purchase.postage_id
                INNER JOIN Customer ON Customer.id = Purchase.customer_id
                INNER JOIN Customer_Address ON Customer_Address.customer_id =
                    Customer.id
                INNER JOIN Address ON Address.id = Customer_Address.address_id
            WHERE
                Purchase.id >= ?
            ORDER BY
                Status.id
        ''', (self._new_order_pointer,))
        return queryset.fetchall()

    def update_database(self):
        '''Uploads changes to order data to database on exit of app.

        Needs references of Order instances that have been updated so is
        retrieved from OrderController - having to import here to avoid
        circular import error; a drawback from including an event listener
        on exit of app. Does however mean that database isn't updated every
        time an order is changed uncessarily - improving performance.
        '''
        from ..controllers.order_controller import OrderController

        def get_status_id(status):
            # Finds the corresponding ID by status description.
            queryset = self._data_access.execute('''
                SELECT
                    Status.id
                FROM
                    Status
                WHERE
                    Status.status_description = ?
            ''', (status,)).fetchone()
            return int(queryset[0])

        for order in OrderController.updated_orders:
            order_key = list(order.keys())[0]
            order_obj = order[order_key]
            status_id = get_status_id(order_obj.status)
            purchase_id = int(order_key.split('_')[1])
            dispatched_date = order_obj.dispatched_date
            completed_date = order_obj.completed_date

            self._data_access.execute('''
                UPDATE
                    Purchase
                SET
                    status_id = ?,
                    dispatched_date = ?,
                    completed_date = ?
                WHERE
                    id = ?
            ''', (status_id, dispatched_date, completed_date, purchase_id))
