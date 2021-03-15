import atexit
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from order_management.presentation.order_management.order_management_view import OrderManagementScreen
from order_management.data.query import Query


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("order_management/presentation/main.kv")
        self._query = Query()

    def build(self):
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        # The below screen manager calling/instantiating the OrderController.py class again, (the init method of this did also)
        sm = ScreenManager()
        sm.add_widget(OrderManagementScreen(name='order_management'))
        return self.screen

    def update_database(self):
        self._query.update_database()

if __name__ == "__main__":
    MainApp().run()
    main_app = MainApp()
    atexit.register(main_app.update_database)
