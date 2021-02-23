from .initialise import Initialise
from .order import Order
from .pdf import Pdf

class PickingList:
    def __init__(self):
        self.initialise = Initialise()
        self.pdf = Pdf()
        self.ids = []
        self.product_descriptions = []
        self.quantities = []

    def create_picking_list(self):
        # product id, aisle, shelf, description, quantity, space for tick
        awaiting_orders = [order for order in self.initialise.orders.values() if order.status == "Awaiting"]
        ordered_items = [product for order in awaiting_orders for product in order.product.ordered_items]
        ordered_items.sort(key=lambda product: (product['aisle'], product['shelf']))

        grouped_items = []
        grouped_items_position = -1

        for index, product in enumerate(ordered_items):
            previous = ordered_items[index-1]
            if index == 0:
                grouped_items.append(product)
                grouped_items_position += 1
            elif product['item_id'] == previous['item_id']:
                grouped_items[grouped_items_position]['quantity'] = \
                    grouped_items[grouped_items_position]['quantity'] + product['quantity']
            else:
                grouped_items.append(product)
                grouped_items_position += 1
        self.pdf.write_pdf()
        return grouped_items
            