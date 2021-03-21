import os, shutil
from .constants import PACKAGING_LIST_DIR, ADDRESS_LABELS_DIR
from .controllers.request_controller import RequestController
from .controllers.order_controller import OrderController
from .data.query import Query
from .document import Document
from .print import Print


class Main:
    def __init__(self):
        self._query = Query()
        self._request_controller = RequestController()
        self._order_controller = OrderController()
        self._document = Document()
        self._orders = {}
        self._load_initial_orders()

    def _load_initial_orders(self):
        new_orders_list = self._request_controller.get_new_orders()
        if new_orders_list is not None:
            self._submit_new_orders(new_orders_list)
        all_data = self._query.get_all_data()
        if all_data != []:
            self._orders = self._order_controller.initialise_orders(all_data)

    def _load_new_orders(self):
        new_orders_list = self._request_controller.get_new_orders()
        if new_orders_list is not None:
            # Only retrieve data when have received new orders.
            updated_data = self._query.get_new_data()
            return self._order_controller.initialise_orders(updated_data)

    def _submit_new_orders(self, new_orders):
        for order in new_orders:
            self._query.add_order(*order)

    def get_initial_table_data(self):
        return self._order_controller.get_table_data()

    def get_new_table_data(self):
        new_order_instances = self._load_new_orders()
        if new_order_instances is not None:
            return self._order_controller.get_table_data()

    def get_order_details(self, order_id):
        return self._order_controller.get_order_details(order_id)

    def update_order_status(self, orders_selected):
        for order in orders_selected:
            self._order_controller.update_order_status(order)
        self._orders = self._order_controller._orders
        return self._order_controller.get_table_data()

    def picking_list(self):
        if len(self._orders) == 0:
            dialog_title = 'There Are Items To Be Picked'
            dialog_body = "There aren't any orders listed as awaiting."
        else:
            self._document.create_picking_list(self._orders.values())
            dialog_title = 'Picking list successfully created!'
            dialog_body = 'You can find the pdf under the picking_list directory'
        return dialog_title, dialog_body

    def packaging_lists(self, orders_selected):
        self._clear_directory(PACKAGING_LIST_DIR)
        for order in orders_selected:
            order_instance = self._orders['order_' + order[0]]
            products_and_quantities = self._order_controller.get_product_quantities(order_instance)
            self._document.create_packaging_list(order_instance, products_and_quantities)
        dialog_title = 'Packaging lists successfully created!'
        dialog_body = 'You can find the pdfs under the packaging_lists directory'
        return dialog_title, dialog_body

    def address_labels(self, orders_selected):
        self._clear_directory(ADDRESS_LABELS_DIR)
        for order in orders_selected:
            order_instance = self._orders['order_' + order[0]]
            self._document.create_address_label(order_instance)
        dialog_title = 'The Address PDFs are in the address_labels directory. Select printer...'
        return dialog_title

    def _clear_directory(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def get_printers(self):
        return Print.all_printers

    def print_pdf(self):
        return Print.print_pdf
