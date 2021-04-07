'''Main Kivy app.

This instantiates a KivyMDApp and loads the main .kv file as well as adding
screens to be loaded. This module should be run as main:

    Typical usage example:

    App().run()
'''
import atexit
import os
import sys
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from order_management.constants import HELP_TEXT
from order_management.presentation.order_management_screen. \
    order_management_view import OrderManagementScreen
from order_management.presentation.components.dialog import Dialog
from order_management.data.query import Query


class App(MDApp):
    '''Creates a KivyMD app and adds the OrderManagementScreen.

    The main.kv file is loaded with the base styling and when run as main
    will set an event listener for on exit to upload changes to orders.

    Attributes:
        screen: reference to context of all rendered elements.
    '''

    def __init__(self, **kwargs):
        '''Inits App

        Args:
            **kwargs: used to inherit MDApp properties.
        '''
        super().__init__(**kwargs)
        self.screen = Builder.load_file(
            "order_management/presentation/main.kv")
        self._query = Query()
        self._dialog = Dialog()

    def build(self):
        '''Additional configurations for MDApp.

        Sets a green colour pallete and adds OrderManagementScreen.

        Returns:
            A KivyMD class with added elements from OrderManagementScreen.

            All attributes of this can be viewed in the debugger, any
            usable attributes will be public denoted by a variable name
            starting without an underscore.
        '''
        self.theme_cls.primary_palette = "Green"
        sm = ScreenManager()
        # Instantiates OrderManagementScreen.py
        sm.add_widget(OrderManagementScreen(name='order_management'))
        return self.screen

    def handle_menu_click(self):
        '''Renders dialog/popup with instructions for app usage.

        Is invoked when help icon in top right of screen is clicked.

        Placed in main app because is apart of Toolbar which is a dynamic Kivy
        widget, so the way that it is declared means it can be reused
        across any future screens.
        '''
        self._dialog.render_dialog("Usage Guide:", HELP_TEXT, None, None)

    def update_database(self):
        '''Uploads updated orders to database.

        Invoked when app is quit. Placed in main app because is needed
        to be called on exit.
        '''
        order_management_screen = self.root.children[0].manager.get_screen(
            'order_management')
        order_management_screen.update_database()


if __name__ == "__main__":
    app = App()
    app.run()
    atexit.register(app.update_database)  # Calls update_database on exit.
