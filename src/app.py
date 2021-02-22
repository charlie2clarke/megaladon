from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from presentation.order_management.order_management_view import OrderManagementScreen
from kivy.clock import Clock
# from kivy.core.window import Window

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file("./presentation/main.kv")

    def build(self):
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        # The below screen manager calling/instantiating the initialise.py class again, (the init method of this did also)
        sm = ScreenManager()
        sm.add_widget(OrderManagementScreen(name='order_management'))
        # Clock.schedule_once(self.order_management_view.create_order_table)
        return self.screen

if __name__ == "__main__":
    # Window.fullscreen = True
    MainApp().run()
