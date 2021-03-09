from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.metrics import dp
from kivy.clock import Clock
from threading import Timer
from functools import partial
from business_logic.table import Table
from business_logic.picking_list import PickingList
from business_logic.packaging_list import PackagingList
from business_logic.address_label import AddressLabel
from business_logic.order_controller import OrderController
from business_logic.order import Order
from ..components.data_table import DataTable


class OrderManagementScreen(Screen):
    _intialise_counter = 0

    def __init__(self, **kwargs):
        super(OrderManagementScreen, self).__init__(**kwargs)
        OrderManagementScreen._intialise_counter += 1
        self._picking_list = PickingList()
        self._packaging_list = PackagingList()
        self._address_label = AddressLabel()
        self._table = Table()
        self._data_table = DataTable()
        # creating order member variable because is needed to access instance method
        # for rendering the order details and the dialog kivy widget must be referenced
        # as a class instance.
        self._order = Order(None, None, None, None, None, None, None)
        self._rows_checked = []
        self._order_table = None
        self._check_pressed = False
        # Class is instantiated once through python and once through Kivy, so
        # am making sure the costly database call is only invoked once.
        if OrderManagementScreen._intialise_counter == 1:
            # Is calling the intial creation of the table. Uses the schedule_once function
            # to await for creation of kivy widgets so can add table to screen.
            Clock.schedule_once(partial(self.create_order_table, False, False, False))
            # Asynchronous thread to refresh orders every minute.
            Clock.schedule_interval(partial(self.create_order_table, True, False, True), 10)

    def create_order_table(self, reset, reset_checks, new_api_call, clock):
        # Clock is an argument passed from the Clock.schedule_once call.
        if reset or reset_checks:
            self.ids.table_container.clear_widgets()

        if reset_checks == False:
            self.row_data = self._table.get_table_data(new_api_call)
            self.column_data = [
                ('No.', dp(30)),
                ('Customer', dp(30)),
                ('Order Date', dp(30)),
                ('Status', dp(30)),
                ('Total Gross', dp(30)),
            ]
        self._order_table = self._data_table.create_data_table(
            self.column_data, self.row_data, self.on_row_press, self.on_check_press)

        # Defining member variable here so that instance of this screen passes the
        # data table as a parameter.
        self._order_controller = OrderController(self)

        self.ids.table_container.add_widget(self._order_table)

    def enable_buttons(self):
        self.ids.packaging_list_button.disabled = False
        self.ids.address_label_button.disabled = False
        self.ids.status_button.disabled = False

    def disable_buttons(self):
        self.ids.packaging_list_button.disabled = True
        self.ids.address_label_button.disabled = True
        self.ids.status_button.disabled = True

    def clear_checked(self):
        self._rows_checked = []
        self.disable_buttons()
        self.create_order_table(False, True, None, False)

    def handle_picking_click(self):
        self._picking_list.create_picking_list()

    def handle_packaging_click(self):
        self._packaging_list.create_packaging_list(self._rows_checked)
        self.clear_checked()

    def handle_address_click(self):
        self._address_label.create_address_label(self._rows_checked)
        self.clear_checked()

    def handle_status_click(self):
        self._order_controller.update_order(self._rows_checked)
        self.clear_checked()

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked. SHOULD DISPLAY MORE DETAILS OF THE ORDER CLICKED ON '''
        
        if self._check_pressed == False:
            # Getting the order id from the row as instance row only returns
            # the text of the column clicked
            index = instance_row.index
            row_data = instance_table.row_data[index]
            order_id = row_data[0]
            self._order.get_order_details(order_id)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked. WILL HANDLE CREATING A PACKING LIST, ADDRESS LABELS, 
        UPDATING STATUS AND CREATING PERSONALISED EMAILS FOR EACH BOX CLICKED '''
        def set_checked_press():
            self._check_pressed = False
    
        self._check_pressed = True
        Timer(1.0, set_checked_press)
        if current_row in self._rows_checked:
            self._rows_checked.remove(current_row)
        else:
            self._rows_checked.append(current_row)
        
        if len(self._rows_checked) > 0:
            self.enable_buttons()
        else:
            self.disable_buttons()

