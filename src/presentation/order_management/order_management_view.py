from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from business_logic.table import Table


class OrderManagmentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = Table()
        # self.order = Order()
        # self.data = self.order.get_order_table_data()
    
    def on_pre_enter(self):
        self.create_order_table()

    def create_order_table(self):
        table_data = self.table.get_table_data()

        self.data_table = MDDataTable(
            size_hint=(1, 1),
            pos_hint={'right': 0.8},
            use_pagination=True,
            check=True,

            column_data= [
                ('Item', dp(30)),
                ('Quantity', dp(30)),
                ('Customer', dp(30)),
                ('Status', dp(30)),
            ],
            row_data=table_row_data
        
        )
