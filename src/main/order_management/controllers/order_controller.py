'''Controls logic for associated with Order instances.

Also provides helper functions for orders, such as getting the total price,
and formats order data appropriately.
'''
from datetime import datetime
from collections import Counter
from ..models.product import Product
from ..models.address import Address
from ..models.customer import Customer
from ..models.order import Order
from .. import outlook_email


class OrderController:
    '''A class to control the logic for Order instances.

    Stores all instances of Order and provides generic helper functions
    and formatting.

    Attributes:
        updated_orders: an array of Order instances of that have had their
                        status updated.
    '''

    def __init__(self):
        '''Inits OrderController.

        Storing instances of order as dictionaries with id as key
        and order instance as value - allows for more efficient look up
        of order by id.
        '''
        self._orders = {}
        self._updated_orders = []

    @property
    def orders(self):
        '''Dictionary with id as key and Order instance as value.

        Have made this private because orders should be accessed
        through Main.
        '''
        return self._orders

    @property
    def updated_orders(self):
        return self._updated_orders

    def get_total_price(self, ordered_items):
        # Will sum the price of all products in order
        # to retrieve total.
        total = 0

        for product in ordered_items:
            total = total + product.price
        return total

    def get_product_quantities(self, order):
        '''For an instance of Order groups items and finds quantities.

        Args:
            order: instance of Order.

        Returns:
            A dictionary with items as key and quantity as value.
        '''
        products = [product.product_name for product in order.products]
        products_and_quantities = dict(Counter(products))
        return products_and_quantities

    def initialise_orders(self, order_queryset):
        '''Instantiates Order instances.

        Using order_queryset, orders are grouped with a check-back comparison
        and instances of Order are out in self._orders.

        Args:
            order_queryset: an array of database rows retrieved - each row a
            nested array.

        Returns:
            A dictionary of all orders with order id as key and Order instance
            as value.
        '''

        # An array of Product instances - one instance for each product.
        products = []

        for i in range(len(order_queryset) + 1):
            if i == 0:
                # first item - append
                quantity = order_queryset[i][2]

                for j in range(quantity):
                    products.append(Product(product_id=order_queryset[i][16],
                                            product_name=order_queryset[i][1],
                                            price=order_queryset[i][15],
                                            aisle=order_queryset[i][17],
                                            shelf=order_queryset[i][18]))

                address = Address(line_one=order_queryset[i][6],
                                  line_two=order_queryset[i][7],
                                  city=order_queryset[i][8],
                                  postcode=order_queryset[i][9])
                customer = Customer(address=address,
                                    first_name=order_queryset[i][3],
                                    last_name=order_queryset[i][4],
                                    email=order_queryset[i][5])
            elif i == len(order_queryset):
                # is the last order then submit
                quantity = order_queryset[i-1][2]

                for j in range(quantity):
                    products.append(Product(product_id=order_queryset[i-1][16],
                                            product_name=order_queryset[i-1]
                                                                       [1],
                                            price=order_queryset[i-1][15],
                                            aisle=order_queryset[i-1][17],
                                            shelf=order_queryset[i-1][18]))
                address = Address(line_one=order_queryset[i-1][6],
                                  line_two=order_queryset[i-1][7],
                                  city=order_queryset[i-1][8],
                                  postcode=order_queryset[i-1][9])
                customer = Customer(address=address,
                                    first_name=order_queryset[i-1][3],
                                    last_name=order_queryset[i-1][4],
                                    email=order_queryset[i-1][5])
                self._orders["order_" + str(order_queryset[i-1][0])] = \
                    Order(order_id=order_queryset[i-1][0],
                          products=products, customer=customer,
                          status=order_queryset[i-1][10],
                          created_date=order_queryset[i-1][11],
                          dispatched_date=order_queryset[i-1][12],
                          completed_date=order_queryset[i-1][13],
                          postage=order_queryset[i-1][14])
            elif order_queryset[i][0] == order_queryset[i-1][0]:
                # is the same order as the one before it
                quantity = order_queryset[i][2]

                for j in range(quantity):
                    products.append(Product(product_id=order_queryset[i][16],
                                            product_name=order_queryset[i][1],
                                            price=order_queryset[i][15],
                                            aisle=order_queryset[i][17],
                                            shelf=order_queryset[i][18]))
            else:
                # new order, so firstly submit the previous order and then add
                # details of new order, unless the next item is the last one.
                address = Address(line_one=order_queryset[i-1][6],
                                  line_two=order_queryset[i-1][7],
                                  city=order_queryset[i-1][8],
                                  postcode=order_queryset[i-1][9])
                customer = Customer(address=address,
                                    first_name=order_queryset[i-1][3],
                                    last_name=order_queryset[i-1][4],
                                    email=order_queryset[i-1][5])
                self._orders["order_" + str(order_queryset[i-1][0])] = \
                    Order(order_id=order_queryset[i-1][0],
                          products=products,
                          customer=customer,
                          status=order_queryset[i-1][10],
                          created_date=order_queryset[i-1][11],
                          dispatched_date=order_queryset[i-1][12],
                          completed_date=order_queryset[i-1][13],
                          postage=order_queryset[i-1][14])
                products = []  # Reset products.

                # If next one is not the last one, add new Product instance
                # to products.
                if i + 1 != len(order_queryset):
                    quantity = order_queryset[i][2]

                    for j in range(quantity):
                        products.append(Product(
                            product_id=order_queryset[i][16],
                            product_name=order_queryset[i][1],
                            price=order_queryset[i][15],
                            aisle=order_queryset[i][17],
                            shelf=order_queryset[i][18]))

        return self._orders

    def get_table_data(self):
        '''Format Order instance data for use in MDDataTable.

        Returns:
            An array with a tuple for each table row - every item a string.
        '''
        # row_data format (in each tuple of table_data):
        # order number, customer, order date, status, total gross.
        table_data = []
        order_number = 0

        for order in self._orders:
            order_number = order.split('_')[1]  # should be the id

            row_data = []
            order_instance = self._orders[order]
            customer_name = order_instance.customer.first_name + \
                ' ' + order_instance.customer.last_name

            row_data.append(str(order_number))
            row_data.append(customer_name)
            row_data.append(order_instance.created_date)
            row_data.append(order_instance.status)
            row_data.append(
                '£' + str(self.get_total_price(order_instance.products)))
            table_data.append(tuple(row_data))

        return table_data

    def get_order_details(self, order_id):
        '''Formats Order instance data for a single order.

        Is used for dialog/modal/popup on_row_press of data table.

        Args:
            order_id: string of order id retrieved from row pressed of which
            to get details of.

        Returns:
            A tuple with first item as dialog title and second as body text.
            Body text includes customer, items ordered and dates.
        '''
        order_instance = self._orders['order_' + order_id]
        product_and_quantities = self.get_product_quantities(order_instance)
        ordered_items = ["  " + str(key) + ' * ' +
                         str(product_and_quantities[key])
                         for key in product_and_quantities]
        ordered_items = '\n'.join(ordered_items)
        name = order_instance.customer.first_name + \
            ' ' + order_instance.customer.last_name
        order_text = 'Customer: {},\n\n' \
            'Ordered items:\n' \
            '{}\n\n' \
            'Order date: {}\n\n' \
            'Dispatched date: {}\n\n' \
            'Completed date: {}'.format(name,
                                        ordered_items,
                                        order_instance.created_date,
                                        order_instance.dispatched_date,
                                        order_instance.completed_date)
        order_title = 'Order number ' + order_id

        return order_title, order_text

    def update_order_status(self, order):
        '''Updates status of single Order instance.

        Will update status from Awaiting to Dispatched,
        and Dispatched to Completed.

        Args:
            order: instance of Order.

        Returns:
            Same Order instance but with updated status.
        '''
        # Sets dispatched/completed date to date now.
        date_now = datetime.today().strftime('%Y-%m-%d')
        if order.status == 'Awaiting':
            order.status = 'Dispatched'
            order.dispatched_date = date_now
        elif order.status == 'Dispatched':
            order.status = 'Complete'
            order.completed_date = date_now
        order_dict = {}
        order_dict['order_' + str(order.order_id)
                   ] = order
        # Add instance of Order to updated_orders so can updates can
        # be uploaded to database on exit of app.
        self._updated_orders.append(order_dict)

        product_and_quantities = self.get_product_quantities(order)
        outlook_email.update_status(
            order, product_and_quantities)
        return order
