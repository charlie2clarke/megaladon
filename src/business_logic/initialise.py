from data.query import Query
from .product import Product
from .address import Address
from .customer import Customer
from .order import Order

class Initialise:
    def __init__(self):
        self.query = Query()
        self.all_data = self.query.get_all_data()
        self.orders = {}
        self.initialise_classes()

    def initialise_classes(self):
        # return self.all_data
        order = []

        def append_order(item, quantity):
            order_entry = {}

            order_entry['item'] = item
            order_entry['quantity'] = quantity
            
            return order_entry

        for i in range(len(self.all_data) + 1):
            order_entry = {}
            if i == 0:
                # first item - append
                order.append(append_order(self.all_data[i][1], self.all_data[i][2]))

                address = Address(line_one=self.all_data[i][6], line_two=self.all_data[i][7], \
                    city=self.all_data[i][8], postcode=self.all_data[i][9])
                customer = Customer(address=address, first_name=self.all_data[i][3], \
                    last_name=self.all_data[i][4], email=self.all_data[i][5])
            elif i == len(self.all_data):
                # is the same order as the one before it
                order.append(append_order(self.all_data[i-1][1], self.all_data[i-1][2]))
                # then submit
                product = Product(items_and_quantity=order)
                address = Address(line_one=self.all_data[i-1][6], line_two=self.all_data[i-1][7], \
                    city=self.all_data[i-1][8], postcode=self.all_data[i-1][9])
                customer = Customer(address=address, first_name=self.all_data[i-1][3], \
                    last_name=self.all_data[i-1][4], email=self.all_data[i-1][5])
                self.orders["order_" + str(i-1)] = Order(product=product, customer=customer, status=self.all_data[i-1][10], \
                    created_date=self.all_data[i-1][11], dispatched_date=self.all_data[i-1][12], \
                        completed_date=self.all_data[i-1][13], postage=self.all_data[i-1][14])   
            elif self.all_data[i][0] == self.all_data[i-1][0]:
                # is the same order as the one before it
                order.append(append_order(self.all_data[i][1], self.all_data[i][2]))
            else:
                # new order
                product = Product(items_and_quantity=order)
                address = Address(line_one=self.all_data[i-1][6], line_two=self.all_data[i-1][7], \
                    city=self.all_data[i-1][8], postcode=self.all_data[i-1][9])
                customer = Customer(address=address, first_name=self.all_data[i-1][3], \
                    last_name=self.all_data[i-1][4], email=self.all_data[i-1][5])
                self.orders["order_" + str(i-1)] = Order(product=product, customer=customer, status=self.all_data[i-1][10], \
                    created_date=self.all_data[i-1][11], dispatched_date=self.all_data[i-1][12], \
                        completed_date=self.all_data[i-1][13], postage=self.all_data[i-1][14])
                order = []

                if i + 1 != len(self.all_data):
                    order.append(append_order(self.all_data[i][1], self.all_data[i][1]))

        return self.orders

    




    
