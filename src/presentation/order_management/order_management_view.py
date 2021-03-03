from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.metrics import dp
from kivy.clock import Clock
from functools import partial
from business_logic.table import Table
from business_logic.picking_list import PickingList
from business_logic.packaging_list import PackagingList
from business_logic.address_label import AddressLabel
from business_logic.order_controller import OrderController
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
        self._rows_checked = []
        self._order_table = None

        # Class is instantiated once through python and once through Kivy, so
        # am making sure the costly database call is only invoked once.
        if OrderManagementScreen._intialise_counter == 1:
            Clock.schedule_once(partial(self.create_order_table, None))

    def create_order_table(self, reset, clock):
        # Clock is an argument passed from the Clock.schedule_once call.
        if reset:
            self.ids.table_container.clear_widgets()

        self.row_data = self._table.get_table_data()
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

    def handle_picking_click(self):
        self._picking_list.create_picking_list()

    def handle_packaging_click(self):
        self._packaging_list.create__packaging_list(self._rows_checked)

    def handle_address_click(self):
        self._address_label.create__address_label(self._rows_checked)

    def handle_status_click(self):
        self._order_controller.update_order(self._rows_checked)

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked. SHOULD DISPLAY MORE DETAILS OF THE ORDER CLICKED ON '''
        print("ROW")
        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked. WILL HANDLE CREATING A PACKING LIST, ADDRESS LABELS, 
        UPDATING STATUS AND CREATING PERSONALISED EMAILS FOR EACH BOX CLICKED '''
        self._rows_checked.append(current_row)
        print("CHECK")
        print(instance_table, current_row)
