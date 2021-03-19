import json
import requests
from collections import Counter
from ..constants import WEBAY_URL

 
class RequestController:
    def __init__(self):
        self._new_orders = []

    def get_new_orders(self):
        self._new_orders = []

        def get_name(order):
            return order['name'].split(' ', 1)[0], order['name'].split(' ', 1)[1]

        def get_address(order):
            address = order['address'].split(', ')
            if len(address) == 2:
                # No line two of address
                return address[0], None, address[1]
            else:
                return address[0], address[1], address[2]

        def get_fake_email(first_name, last_name):
            return (first_name.lower() + '.' + last_name.lower()).replace(' ', '') + '@gmail.com'

        def get_items_and_quantity(item_counter):
            items_and_quantity = []

            for item in item_counter:
                new_order_entry = {}
                new_order_entry['item'], new_order_entry['quantity'] = item[0], item[1]
                items_and_quantity.append(new_order_entry)

            return items_and_quantity

        try:
            # first timeout value is connect and second is read
            request = requests.get(WEBAY_URL, timeout=(2, 4))
            request_string = request.text
            request_json = json.loads(request_string)

            if request_json != [] and request.status_code == 200:
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
                        items.append(request_json[index]['item'])
                    elif index == len(request_json):
                        if len(items) > 1 or len(request_json) == 1:
                            # The last one is for the same order as previous
                            items_and_quantity = get_items_and_quantity(
                                item_counter)
                            fake_email = get_fake_email(
                                previous_first_name, previous_last_name)
                            order_entry = [items_and_quantity, previous_first_name, previous_last_name,
                                                 previous_address_line_one, previous_address_line_two, previous_city, fake_email, index]
                            self._new_orders.append(order_entry)
                        else:
                            # last order is for a new person
                            items.append(request_json[index - 1]['item'])
                            item_counter = Counter(items).items()
                            items_and_quantity = get_items_and_quantity(
                                item_counter)
                            fake_email = get_fake_email(
                                previous_first_name, previous_last_name)
                            order_entry = [items_and_quantity, previous_first_name, previous_last_name,
                                                 previous_address_line_one, previous_address_line_two, previous_city, fake_email, index]
                            self._new_orders.append(order_entry)
                    elif first_name == previous_first_name and last_name == previous_last_name and \
                        address_line_one == previous_address_line_one and address_line_two == previous_address_line_two \
                            and city == previous_city:
                        items.append(request_json[index]['item'])
                    else:
                        items_and_quantity = get_items_and_quantity(
                            item_counter)
                        fake_email = get_fake_email(
                            previous_first_name, previous_last_name)
                        order_entry = [items_and_quantity, previous_first_name, previous_last_name,
                                                 previous_address_line_one, previous_address_line_two, previous_city, fake_email, index]
                        self._new_orders.append(order_entry)

                        items = []
                        if index + 1 != len(request_json):
                            items.append(request_json[index]['item'])
            return self._new_orders
        except requests.exceptions.Timeout as error_t:
            print("Timeout: " + str(error_t))
        except requests.exceptions.ConnectionError as error_c:
            print("ConnectionError " + str(error_c))
        except requests.exceptions.HTTPError as error_h:
            print("HTTPError: " + str(error_h))
