from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from business_logic.order.order import Order


class OrderManagmentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def load_table_data(self):
        order = Order()
        test = order.get_order_table_data()
        print(test)
