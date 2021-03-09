from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
import atexit
from presentation.order_management.order_management_view import OrderManagementScreen
from data.query import Query


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("./presentation/main.kv")
        self.query = Query()

    def build(self):
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        # The below screen manager calling/instantiating the OrderController.py class again, (the init method of this did also)
        sm = ScreenManager()
        sm.add_widget(OrderManagementScreen(name='order_management'))
        self.menu = MDDropdownMenu(
            caller=self.screen.current_screen.children[0].ids.toolbar_button,
            items=[
                {'text': 'Account'},
                {'text': 'Help'}
            ],
            width_mult=4
        )
        self.menu.bind(on_release=self.handle_menu_item_click)
        return self.screen

    def handle_menu_click(self):
        self.menu.open()

    def handle_menu_item_click(self):
        print(menu)
        print(item)

    def update_database(self):
        self.query.update_database()

if __name__ == "__main__":
    # Window.fullscreen = True
    MainApp().run()
    main_app = MainApp()
    atexit.register(main_app.update_database)
