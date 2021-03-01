import json
import requests
from collections import Counter
from data.query import Query
from .product import Product
from .address import Address
from .customer import Customer
from .order import Order


class OrderController:
    order_controller_counter = 0
    orders = {}

    def __init__(self):
        OrderController.order_controller_counter += 1
        self.query = Query()
        # self.orders = {} # I should make this a class variable?!
        self.new_orders = {}

        if OrderController.order_controller_counter == 1:
            self.get_new_orders()
            self.all_data = self.query.get_all_data()
            self.initialise_orders()  # I should make this a class variable?!

    def get_new_orders(self):
        url = 'http://localhost:8080'

        def get_name(order):
            return order['name'].split(' ', 1)[0], order['name'].split(' ', 1)[1]

        def get_address(order):
            address = order['address'].split(', ')
            if len(address) == 2:
                # No line two of address
                return address[0], None, address[1]
            else:
                return address[0], address[1], address[2]

        def get_items_and_quantity(item_counter):
            items_and_quantity = []

            for item in item_counter:
                new_order_entry = {}
                new_order_entry['item'], new_order_entry['quantity'] = item[0], item[1]
                items_and_quantity.append(new_order_entry)
            
            return items_and_quantity

        try:
            request = requests.get(url)
            request_string = request.text
            request_json = json.loads(request_string)

            if request_json != []:
                request_json.sort(key=lambda order: order['name'])
                # [{first_name: x, last_name: x, email: x, line_one: x, line_two: x, city: x, items: [x, y]}]
                items = []
                for index in range(len(request_json) + 1):
                    item_counter = Counter(items).items()

                    if index != len(request_json):
                        first_name, last_name = get_name(request_json[index])
                        address_line_one, address_line_two, city = get_address(
                            request_json[index])
                    previous_order = request_json[index - 1]

                    if index != 0:
                        previous_first_name, previous_last_name = get_name(
                            previous_order)
                        previous_address_line_one, previous_address_line_two, previous_city = get_address(
                            previous_order)

                    if index == 0:
                        # new_order.append(append_order(order['item'], first_name, last_name, address_line_one, address_line_two, city))
                        items.append(request_json[index]['item'])
                    elif index == len(request_json):
                        if len(items) > 1 or len(request_json) == 1:
                            # The last one is for the same order as previous
                            items_and_quantity = get_items_and_quantity(item_counter)
                            self.query.add_order(items_and_quantity, previous_first_name, previous_last_name,
                                             previous_address_line_one, previous_address_line_two, previous_city)
                        else:
                            # last order is for a new person
                            items.append(request_json[index - 1]['item'])
                            item_counter = Counter(items).items()
                            items_and_quantity = get_items_and_quantity(item_counter)
                            self.query.add_order(items_and_quantity, previous_first_name, previous_last_name,
                                                previous_address_line_one, previous_address_line_two, previous_city)
                    elif first_name == previous_first_name and last_name == previous_last_name and \
                        address_line_one == previous_address_line_one and address_line_two == previous_address_line_two \
                            and city == previous_city:
                        items.append(request_json[index]['item'])
                    else:
                        items_and_quantity = get_items_and_quantity(item_counter)
                        self.query.add_order(items_and_quantity, previous_first_name, previous_last_name,
                                             previous_address_line_one, previous_address_line_two, previous_city)

                        items = []
                        if index + 1 != len(request_json):
                            items.append(request_json[index]['item'])

        except requests.exceptions.ConnectionError as error_c:
            print("There seems to be a network problem " + str(error_c))
        except requests.exceptions.HTTPError as error_h:
            print("HTTP error: " + str(error_h))

    def initialise_orders(self):
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

        for i in range(len(self.all_data) + 1):
            if i == 0:
                # first item - append
                order.append(append_order(self.all_data[i][16], self.all_data[i][1], self.all_data[i][2],
                                          self.all_data[i][15], self.all_data[i][17], self.all_data[i][18]))

                address = Address(line_one=self.all_data[i][6], line_two=self.all_data[i][7],
                                  city=self.all_data[i][8], postcode=self.all_data[i][9])
                customer = Customer(address=address, first_name=self.all_data[i][3],
                                    last_name=self.all_data[i][4], email=self.all_data[i][5])
            elif i == len(self.all_data):
                # is the last order
                order.append(append_order(self.all_data[i-1][16], self.all_data[i-1][1], self.all_data[i-1][2],
                                          self.all_data[i-1][15], self.all_data[i-1][17], self.all_data[i-1][18]))
                # then submit
                product = Product(ordered_items=order)
                address = Address(line_one=self.all_data[i-1][6], line_two=self.all_data[i-1][7],
                                  city=self.all_data[i-1][8], postcode=self.all_data[i-1][9])
                customer = Customer(address=address, first_name=self.all_data[i-1][3],
                                    last_name=self.all_data[i-1][4], email=self.all_data[i-1][5])
                OrderController.orders["order_" + str(self.all_data[i-1][0])] = Order(product=product, customer=customer, status=self.all_data[i-1][10],
                                                         created_date=self.all_data[i -
                                                                                    1][11], dispatched_date=self.all_data[i-1][12],
                                                         completed_date=self.all_data[i-1][13], postage=self.all_data[i-1][14])
            elif self.all_data[i][0] == self.all_data[i-1][0]:
                # is the same order as the one before it
                order.append(append_order(self.all_data[i][16], self.all_data[i][1], self.all_data[i][2],
                                          self.all_data[i][15], self.all_data[i][17], self.all_data[i][18]))
            else:
                # new order, so firstly submit the previous order and then add details of new order, unless the
                # next item is the last one
                product = Product(ordered_items=order)
                address = Address(line_one=self.all_data[i-1][6], line_two=self.all_data[i-1][7],
                                  city=self.all_data[i-1][8], postcode=self.all_data[i-1][9])
                customer = Customer(address=address, first_name=self.all_data[i-1][3],
                                    last_name=self.all_data[i-1][4], email=self.all_data[i-1][5])
                OrderController.orders["order_" + str(self.all_data[i-1][0])] = Order(product=product, customer=customer, status=self.all_data[i-1][10],
                                                         created_date=self.all_data[i -
                                                                                    1][11], dispatched_date=self.all_data[i-1][12],
                                                         completed_date=self.all_data[i-1][13], postage=self.all_data[i-1][14])
                order = []

                if i + 1 != len(self.all_data):
                    order.append(append_order(self.all_data[i][16], self.all_data[i][1], self.all_data[i][2],
                                              self.all_data[i][15], self.all_data[i][17], self.all_data[i][18]))

