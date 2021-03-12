from datetime import datetime
from models.product import Product
from models.address import Address
from models.customer import Customer
from models.order import Order
import outlook_email


class OrderController:
    updated_orders = []

    def __init__(self):
        # Storing instances of order as list of dictionaries with id as key
        # and order instance as value - allows for more efficient look up
        # of order by id.
        self._orders = {}

    @property
    def orders(self):
        return self._orders

    def initialise_orders(self, order_queryset):
        order = []

        def append_order(item_id, item, quantity, individual_price, aisle, shelf):
            order_entry = {}

            order_entry['item_id'] = item_id
            order_entry['item'] = item
            order_entry['quantity'] = quantity
            order_entry['individual_price'] = individual_price
            order_entry['aisle'] = aisle
            order_entry['shelf'] = shelf

            return order_entry

        for i in range(len(order_queryset) + 1):
            if i == 0:
                # first item - append
                order.append(append_order(order_queryset[i][16], order_queryset[i][1], order_queryset[i][2],
                                          order_queryset[i][15], order_queryset[i][17], order_queryset[i][18]))

                address = Address(line_one=order_queryset[i][6], line_two=order_queryset[i][7],
                                  city=order_queryset[i][8], postcode=order_queryset[i][9])
                customer = Customer(address=address, first_name=order_queryset[i][3],
                                    last_name=order_queryset[i][4], email=order_queryset[i][5])
            elif i == len(order_queryset):
                # is the last order
                order.append(append_order(order_queryset[i-1][16], order_queryset[i-1][1], order_queryset[i-1][2],
                                          order_queryset[i-1][15], order_queryset[i-1][17], order_queryset[i-1][18]))
                # then submit
                product = Product(ordered_items=order)
                address = Address(line_one=order_queryset[i-1][6], line_two=order_queryset[i-1][7],
                                  city=order_queryset[i-1][8], postcode=order_queryset[i-1][9])
                customer = Customer(address=address, first_name=order_queryset[i-1][3],
                                    last_name=order_queryset[i-1][4], email=order_queryset[i-1][5])
                self._orders["order_" + str(order_queryset[i-1][0])] = Order(order_id=order_queryset[i-1][0], product=product, customer=customer, status=order_queryset[i-1][10],
                                                                             created_date=order_queryset[i -
                                                                                                         1][11], dispatched_date=order_queryset[i-1][12],
                                                                             completed_date=order_queryset[i-1][13], postage=order_queryset[i-1][14])
            elif order_queryset[i][0] == order_queryset[i-1][0]:
                # is the same order as the one before it
                order.append(append_order(order_queryset[i][16], order_queryset[i][1], order_queryset[i][2],
                                          order_queryset[i][15], order_queryset[i][17], order_queryset[i][18]))
            else:
                # new order, so firstly submit the previous order and then add details of new order, unless the
                # next item is the last one
                product = Product(ordered_items=order)
                address = Address(line_one=order_queryset[i-1][6], line_two=order_queryset[i-1][7],
                                  city=order_queryset[i-1][8], postcode=order_queryset[i-1][9])
                customer = Customer(address=address, first_name=order_queryset[i-1][3],
                                    last_name=order_queryset[i-1][4], email=order_queryset[i-1][5])
                self._orders["order_" + str(order_queryset[i-1][0])] = Order(order_id=order_queryset[i-1][0], product=product, customer=customer, status=order_queryset[i-1][10],
                                                                             created_date=order_queryset[i -
                                                                                                         1][11], dispatched_date=order_queryset[i-1][12],
                                                                             completed_date=order_queryset[i-1][13], postage=order_queryset[i-1][14])
                order = []

                if i + 1 != len(order_queryset):
                    order.append(append_order(order_queryset[i][16], order_queryset[i][1], order_queryset[i][2],
                                              order_queryset[i][15], order_queryset[i][17], order_queryset[i][18]))

        return self._orders

    def get_table_data(self):
        # order number, customer, order date, status, total gross
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
                '£' + str(order_instance.product.get_total(order_instance.product.ordered_items)))
            table_data.append(tuple(row_data))

        return table_data

    def get_order_details(self, order_id):
        order_instance = self._orders['order_' + order_id]
        ordered_items = [str(key['item']) + ' * ' + str(key['quantity'])
                         for key in order_instance.product.ordered_items]
        ordered_items = '\n'.join(ordered_items)
        name = order_instance.customer.first_name + \
            ' ' + order_instance.customer.last_name
        order_text = 'Customer: {},\n\n' \
            'Ordered items:\n' \
            '   {}\n\n' \
            'Order date: {}\n\n' \
            'Dispatched date: {}\n\n' \
            'Completed date: {}\n\n'.format(name, ordered_items, order_instance.created_date,
                                          order_instance.dispatched_date, order_instance. completed_date)
        order_title = 'Order number ' + order_id

        return order_title, order_text

    def update_order_status(self, order):
        date_now = datetime.today().strftime('%Y-%m-%d')
        if order[3] == 'Awaiting':
            self._orders['order_' +
                         order[0]].status = 'Dispatched'
            self._orders['order_' +
                         order[0]].dispatched_date = date_now
        elif order[3] == 'Dispatched':
            self._orders['order_' + order[0]].status = 'Complete'
            self._orders['order_' +
                         order[0]].completed_date = date_now
        order_dict = {}
        order_dict['order_' + order[0]
                   ] = self._orders['order_' + order[0]]
        OrderController.updated_orders.append(order_dict)
        outlook_email.update_status(
            self._orders['order_' + order[0]])
