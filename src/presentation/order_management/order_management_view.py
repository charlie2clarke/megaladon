from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from business_logic.table import Table
from business_logic.picking_list import PickingList
from business_logic.packaging_list import PackagingList
from business_logic.address_label import AddressLabel
from ..components.dialog import Dialog
# from ..components.data_table import DataTable


class OrderManagementScreen(Screen):
    def __init__(self, **kwargs):
        super(OrderManagementScreen, self).__init__(**kwargs)
        self.picking_list = PickingList()
        self.packaging_list = PackagingList()
        self.address_label = AddressLabel()
        self.dialog = Dialog()
        self.rows_checked = []
        Clock.schedule_once(self.create_order_table)
    
    def create_order_table(self, clock):
        self.table = Table()
        self.row_data = self.table.get_table_data()
        row_number = len(self.row_data)

        # order number, customer, order date, status, total gross
        self.order_table = MDDataTable(
            size_hint=(1, 0.85),
            check=True,
            column_data=[
                ('No.', dp(30)),
                ('Customer', dp(30)),
                ('Order Date', dp(30)),
                ('Status', dp(30)),
                ('Total Gross', dp(30)),
            ],
            row_data=self.row_data,
            rows_num=row_number
        )
        self.order_table.bind(on_row_press=self.on_row_press)
        self.order_table.bind(on_check_press=self.on_check_press)
        
        self.ids.table_container.add_widget(self.order_table)

    def handle_picking_click(self):
        self.picking_list.create_picking_list()

    def handle_packaging_click(self):
        self.packaging_list.create_packaging_list(self.rows_checked)

    def handle_address_click(self):
        self.address_label.create_address_label(self.rows_checked)

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked. SHOULD DISPLAY MORE DETAILS OF THE ORDER CLICKED ON '''
        print("ROW")
        print(instance_table, instance_row)
        # self.dialog.render_dialog('Title', 'some text')
        # self.render_dialog('Title', 'some body text')

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked. WILL HANDLE CREATING A PACKING LIST, ADDRESS LABELS, 
        UPDATING STATUS AND CREATING PERSONALISED EMAILS FOR EACH BOX CLICKED '''
        self.rows_checked.append(current_row)
        print("CHEKC")
        print(instance_table, current_row)

    
