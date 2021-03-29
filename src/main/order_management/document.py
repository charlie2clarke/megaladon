'''Uses order data to format data to be used in:
- Picking list
- Packaging list
- Address label
'''
from collections import Counter
from .pdf import Pdf
from .config import ADDRESS_LABELS_DIR, PACKAGING_LIST_DIR, PICKING_LIST_DIR


class Document:
    '''Uses instances of Order to format data to be input into files.'''
    def __init__(self):
        self._pdf = Pdf()

    def format_address(self, order):
        return [order.customer.first_name + ' ' + order.customer.last_name,
                order.customer.address.line_one, order.customer.address.city]

    def create_picking_list(self, orders):
        '''Formats data from all instances of order with 'Awaiting' status.

        Args:
            orders: list of Order instances.

        Returns:
            A list with header row and a list for each row of order details.
        '''
        awaiting_orders = [order for order in orders if order.status
                           == "Awaiting"]
        ordered_items = [product for order in awaiting_orders for product
                         in order.products]
        # Sorting by aisle and shelf so is in order for picker.
        ordered_items.sort(key=lambda product: (product.aisle, product.shelf))

        grouped_items = []
        grouped_items_position = -1

        for index, product in enumerate(ordered_items):
            previous = ordered_items[index-1]
            if index == 0:
                grouped_items.append([product.product_id, product.product_name,
                                      1, product.price, product.aisle,
                                      product.shelf])
                grouped_items_position += 1
            elif product.product_id == previous.product_id:
                # If same as previous add one to quantity.
                grouped_items[grouped_items_position][2] += 1
            else:
                # Add new entry of item.
                grouped_items.append([product.product_id, product.product_name,
                                      1, product.price, product.aisle,
                                      product.shelf])
                grouped_items_position += 1

        headers = ["Product ID", "Product Name", "Quantity",
                   "Individual Price", "Aisle", "Shelf"]
        picking_table_data = [headers] + grouped_items
        self._pdf.write_picking_list(picking_table_data, PICKING_LIST_DIR)
        return picking_table_data

    def create_packaging_list(self, order, products_and_quantities):
        '''Formats order data for creation of packaging list file.

        Args:
            order: instance of Order to create packaging list of.
            products_and_quantities: dictionary with item key and quantity
            value.

        Returns:
            A tuple with first item as address list with nested list for each
            line, and second item as items list with nested list for each row
            of item details.
        '''
        # date array, address array, items array
        address = self.format_address(order)
        address.insert(0, 'Deliver To:')
        items = [[key, products_and_quantities[key]] for key in
                 products_and_quantities]
        items.insert(0, ['Item', 'Quantity'])

        self._pdf.write_packaging_list(order.created_date, address, items,
                                      order.order_id, PACKAGING_LIST_DIR)
        return address, items

    def create_address_label(self, order):
        '''Formats order data for creation of address labels.

        Args:
            order: instance of Order to create address label of.

        Returns:
            An address list with a nested list for each line.
        '''
        address = self.format_address(order)
        self._pdf.write_address_label(address, order.order_id,
                                     ADDRESS_LABELS_DIR)
        return address
