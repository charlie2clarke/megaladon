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
# from ..components.data_table import DataTable


class OrderManagementScreen(Screen):
    def __init__(self, **kwargs):
        super(OrderManagementScreen, self).__init__(**kwargs)
        self.picking_list = PickingList()
        Clock.schedule_once(self.create_order_table)
     
    def create_order_table(self, clock):
        self.table = Table()
        self.row_data = self.table.get_table_data()

        # order number, customer, order date, status, total gross
        self.order_table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
            column_data=[
                ('No.', dp(30)),
                ('Customer', dp(30)),
                ('Order Date', dp(30)),
                ('Status', dp(30)),
                ('Total Gross', dp(30)),
            ],
            row_data=self.row_data
        )
        self.order_table.bind(on_row_press=self.on_row_press)
        self.order_table.bind(on_check_press=self.on_check_press)
        
        self.ids.table_container.add_widget(self.order_table)

    def handle_picking_click(self):
        self.picking_list.create_picking_list()

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked. SHOULD DISPLAY MORE DETAILS OF THE ORDER CLICKED ON '''
        print(instance_table, instance_row)
        self.render_dialog('Title', 'some body text')

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked. WILL HANDLE CREATING A PACKING LIST, ADDRESS LABELS, 
        UPDATING STATUS AND CREATING PERSONALISED EMAILS FOR EACH BOX CLICKED '''

        print(instance_table, current_row)

    def render_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            size_hint=(0.7, 1),
            text=text,
            buttons=[
                MDRectangleFlatButton(text='Close', on_release=self.close_dialog),
            ]
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
