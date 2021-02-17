from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
# from business_logic.order.order import Order
from business_logic.initialise import Initialise


class OrderManagmentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialise = Initialise()
        # self.order = Order()
        # self.data = self.order.get_order_table_data()
    
    def load_table_data(self):
        print(self.data)
