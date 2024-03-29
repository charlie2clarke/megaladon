'''Python code relating to Kivy OrderManagementScreen.

Kivy automatically relates file based on widget name added to screenmanager.
'''
import asyncio
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.clock import Clock
from functools import partial
from ...main import Main
from ..components.data_table import DataTable
from ..components.dialog import Dialog


class OrderManagementScreen(Screen):
    '''Class that holds reference of Kivy screen properties.

    All kivy widgets held within class are from order_management_ui.kv.
    '''

    _intialise_counter = 0

    def __init__(self, **kwargs):
        '''Inits OrderManagementScreen

        Gets initial data for table and then sets asynchronous call
        to get new table data every minute.

        Args:
            **kwargs: used to inherit MDApp properties.
        '''
        super(OrderManagementScreen, self).__init__(**kwargs)
        OrderManagementScreen._intialise_counter += 1
        # Class is instantiated once through python and once through Kivy, so
        # am making sure the costly database call is only invoked once.
        if OrderManagementScreen._intialise_counter == 1:
            self._main = Main()
            self._dialog = Dialog()
            column_data = [
                ('No.', dp(30)),
                ('Customer', dp(30)),
                ('Order Date', dp(30)),
                ('Status', dp(30)),
                ('Total Gross', dp(30)),
            ]
            self._data_table = DataTable(column_data)
            self.order_table = None
            self.check_pressed = False

            # Is calling the intial creation of the table. Uses the
            # schedule_once function to await for creation of kivy
            # widgets so can add table to screen.
            table_data = self._main.get_initial_table_data()
            Clock.schedule_once(partial(
                self.create_order_table, table_data, False))
            # Asynchronus thread refreshing orders every minute.
            Clock.schedule_interval(self.update_order_table, 60)

    def create_order_table(self, row_data, reset, clock):
        # Clock is an argument passed from the Clock.schedule_once call.
        if reset is True:
            # Deleting table if table with new data needs to be loaded.
            # KivyMDDataTable doesn't currently support dynamically
            # updating data in table, so deleting it and then adding a new one.
            self.ids.table_container.clear_widgets()

        self.order_table = self._data_table.create_data_table(
            row_data, self.on_row_press,
            self.on_check_press)
        self.ids.table_container.add_widget(self.order_table)

    def update_order_table(self, clock):
        # Called every minute to get new order data, if
        # there are new orders then order table is created again.
        table_data = self._main.get_new_table_data()
        if table_data is not None:
            self.create_order_table(table_data, True, None)

    def enable_buttons(self):
        self.ids.packaging_list_button.disabled = False
        self.ids.address_label_button.disabled = False
        self.ids.status_button.disabled = False

    def disable_buttons(self):
        self.ids.packaging_list_button.disabled = True
        self.ids.address_label_button.disabled = True
        self.ids.status_button.disabled = True

    def clear_checked(self, status_updated):
        # Resets selected orders after one of the buttons has been clicked.
        self._data_table.rows_checked = []
        self.disable_buttons()
        # If status is updated, create__order_table is invoked from there.
        if status_updated is False:
            self.create_order_table(None, True, None)

    def handle_picking_click(self):
        '''Handler function when picking list button is released.'''
        dialog_title, dialog_body = self._main.picking_list()
        self._dialog.render_dialog(dialog_title, dialog_body, None, None)

    def handle_packaging_click(self):
        '''Handler function when packaging list button is released.'''
        dialog_title, dialog_body = self._main.packaging_lists(
            self._data_table.rows_checked)
        self._dialog.render_dialog(dialog_title, dialog_body, None, None)
        self.clear_checked(False)

    def handle_address_click(self):
        '''Handler function when address label button is released.'''
        dialog_title = self._main.address_labels(self._data_table.rows_checked)
        available_printers = self._main.get_printers()
        print_pdf = self._main.print_pdf()
        self._dialog.render_dialog(
            dialog_title,
            None,
            available_printers,
            print_pdf)
        self.clear_checked(False)

    def handle_status_click(self):
        '''Handler function when update status button is released.'''
        table_data = self._main.update_order_status(
            self._data_table.rows_checked)
        # await asyncio.wait(table_data)
        self.create_order_table(table_data, True, None)
        self.clear_checked(True)

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.

        Displays details of order selected.

        Args:
            instance_table: instance of MDDataTable.
            instance_row: instance of row of MDDataTable.
        '''
        # Work around for bug in MDDataTable that invokes both row and
        # check press on click of check.
        if self.check_pressed is False:
            # Getting the order id from the row as instance row only returns
            # the text of the column clicked.
            index = instance_row.Index
            row_data = [row for row in instance_table.row_data if row[0]
                        == index]
            order_id = row_data[0][0]
            dialog_title, dialog_body = self._main.get_order_details(order_id)
            self._dialog.render_dialog(dialog_title, dialog_body, None, None)

    def on_check_press(self, instance_table, instance_row):
        '''Called when the check box in the table row is checked.

        Args:
            instance_table: instance of MDDataTable.
            instance_row: instance of row of MDDataTable.
        '''
        def set_checked_press(clock):
            self.check_pressed = False

        self.check_pressed = True
        # Workaround for bug in MDDataTable that invokes both the row and
        # check press on click of check.
        Clock.schedule_once(set_checked_press, 0.5)
        if instance_row in self._data_table.rows_checked:
            self._data_table.rows_checked.remove(instance_row)
        else:
            self._data_table.rows_checked.append(instance_row)

        if len(self._data_table.rows_checked) > 0:
            self.enable_buttons()
        else:
            self.disable_buttons()

    def update_database(self):
        self._main.update_database()
