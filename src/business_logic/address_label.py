from .order_controller import OrderController
from .pdf import Pdf


class AddressLabel:
    def __init__(self):
        self.order_controller = OrderController()
        self.pdf = Pdf()

    def create_address_label(self, orders_selected):
        for index, order in enumerate(orders_selected):
            order_number = int(order[0]) - 1
            order_obj = self.order_controller.orders['order_' + order[0]]

            address = [order_obj.customer.first_name + ' ' + order_obj.customer.last_name,
                       order_obj.customer.address.line_one, order_obj.customer.address.city]

            self.pdf.write_address_label(address, order_number)

