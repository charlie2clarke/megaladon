from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from business_logic.table import Table
from kivy.clock import Clock
from kivymd.uix.button import MDRectangleFlatIconButton


class OrderManagementScreen(Screen):
    def __init__(self, **kwargs):
        super(OrderManagementScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.create_order_table)
      
    def create_order_table(self, clock):
        self.table = Table()
        # order number, customer, order date, status, total gross
        self.table_data = self.table.get_table_data()

        self.data_table = MDDataTable(
            size_hint=(0.95, 0.8),
            # pos_hint={'right': 0.8},
            use_pagination=True,
            check=True,
            column_data=[
                ('No.', dp(30)),
                ('Customer', dp(30)),
                ('Order Date', dp(30)),
                ('Status', dp(30)),
                ('Total Gross', dp(30)),
            ],
            row_data=self.table_data
        )
        
        self.add_widget(self.data_table)
        # self.ids.table_container.add_widget(self.data_table)
