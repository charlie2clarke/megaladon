'''Controls main logic of app.

All public methods are invoked from view in presentation layer.
'''
import os
import shutil
from .config import PACKAGING_LIST_DIR, ADDRESS_LABELS_DIR
from .controllers.request_controller import RequestController
from .controllers.order_controller import OrderController
from .data.query import Query
from .document import Document
from .print import Print


class Main:
    '''Controls main logic.

    Instances of orders held make it the single source of truth.
    '''

    def __init__(self):
        '''Inits Main

        orders is equal to orders of OrderController because of the
        associations of Main - reducing coupling.
        '''
        self._query = Query()
        self._request_controller = RequestController()
        self._order_controller = OrderController()
        self._document = Document()
        self.orders = {}
        self.updated_orders = []
        self._load_initial_orders()

    def _load_initial_orders(self):
        # Loads all orders from database then instantiates
        # Order object through OrderController.
        new_orders_list = self._request_controller.get_new_orders()
        if new_orders_list is not None:
            self._submit_new_orders(new_orders_list)
        all_data = self._query.get_all_data()
        self.orders = self._order_controller.initialise_orders(all_data)

    def _load_new_orders(self):
        # Called every 60 seconds to get new orders.
        new_orders_list = self._request_controller.get_new_orders()
        if new_orders_list is not None:
            # Only retrieve data when have received new orders.
            updated_data = self._query.get_new_data()
            return self._order_controller.initialise_orders(updated_data)

    def _submit_new_orders(self, new_orders):
        # Uploads details of new order to database.
        for order in new_orders:
            self._query.add_order(*order)

    def get_initial_table_data(self):
        '''Get formatted order data for table.'''
        return self._order_controller.get_table_data()

    def get_new_table_data(self):
        '''Loads new orders - if there are new orders gets new formatted
        table data.

        Returns:
            A callback to get formatted order data for table.
        '''
        new_order_instances = self._load_new_orders()
        if new_order_instances is not None:
            return self._order_controller.get_table_data()

    def get_order_details(self, order_id):
        '''For a given order will retrieve formatted details of that order.

        Args:
            order_id: string of order to retrieve details of.

        Returns:
            A callback to get formatted order data for a given order.
        '''
        return self._order_controller.get_order_details(order_id)

    def update_order_status(self, orders_selected):
        '''For each order passed will update instance of order, then re-render
        table to have newest data.

        Args:
            orders_selected: a list of orders (from table) wwith a list for
            each order (all strings).

        Returns:
            A callback to get formatted order data for table.
        '''
        for order in orders_selected:
            order_instance = self.orders['order_' + order[0]]
            self._order_controller.update_order_status(order_instance)
        self.orders = self._order_controller.orders
        self.updated_orders = self._order_controller.updated_orders
        return self._order_controller.get_table_data()

    def picking_list(self):
        '''Controls logic for creating picking list,
        if there are awaiting_orders.

        Returns:
            A tuple with first item as title of dialog/popup
            and second item as contents of dialog/popup.
        '''
        awaiting_orders = [self.orders[order] for order in self.orders
                           if self.orders[order].status == 'Awaiting']
        if len(awaiting_orders) == 0:
            dialog_title = 'There Are No Items To Be Picked'
            dialog_body = "There aren't any orders listed as awaiting."
        else:
            self._document.create_picking_list(self.orders.values())
            dialog_title = 'Picking list successfully created!'
            dialog_body = 'You can find the pdf under the picking_list' \
                          ' directory'
        return dialog_title, dialog_body

    def packaging_lists(self, orders_selected):
        '''Controls logic for creating packaging list for each order passed.

        Args:
            orders_selected: a list of orders from table, with each order
            as a nested list.

        Returns:
            A tuple with first item as title of dialog/popup
            and second item as contents of dialog/popup.
        '''
        self._clear_directory(PACKAGING_LIST_DIR)
        for order in orders_selected:
            order_instance = self.orders['order_' + order[0]]
            # Get dictionary with items as key and quantities as value.
            products_and_quantities = self._order_controller.\
                get_product_quantities(order_instance)
            self._document.create_packaging_list(order_instance,
                                                products_and_quantities)
        dialog_title = 'Packaging lists successfully created!'
        dialog_body = 'You can find the pdfs under the packaging_lists' \
                      ' directory'
        return dialog_title, dialog_body

    def address_labels(self, orders_selected):
        '''Controls logic for creating address labels for each order passed.

        Args:
            orders_selected: a list of orders from table, with each order
            as a nested list.

        Returns:
            A string for the title of a dialog/popup.
        '''
        # Clear any previously made address labels.
        self._clear_directory(ADDRESS_LABELS_DIR)
        for order in orders_selected:
            order_instance = self.orders['order_' + order[0]]
            self._document.create_address_label(order_instance)
        dialog_title = 'The Address PDFs are in the address_labels directory' \
                       '. Select printer...'
        return dialog_title

    def _clear_directory(self, folder):
        # Clears all files with passed 'folder'.
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
        '''Gets details of all available printers from Print.

        Returns:
            Class variable of Print contaning array of all available printers.
        '''
        return Print.all_printers

    def print_pdf(self):
        '''Gets callback to method for printing pdf files.

        Returns:
            A callback to 'print_pdf' method of Print.
        '''
        return Print.print_pdf

    def update_database(self):
        self._query.update_database(self.updated_orders)
