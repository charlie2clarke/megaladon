from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem
from business_logic.print import Print


class Dialog:
    def __init__(self):
        self.print = Print()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def handle_item_click(self, item_clicked):
        self.print.print_pdf(item_clicked.text, 'address_labels')

    def render_dialog(self, title, text, print):
        if print:
            dialog_items = [OneLineAvatarIconListItem(text=str(
                printer), on_release=self.handle_item_click) for printer in Print.all_printers]
            self.dialog = MDDialog(
                title=title,
                size_hint=(0.7, 1),
                type='simple',
                items=dialog_items,
                buttons=[
                    MDRectangleFlatButton(
                        text='Close', on_release=self.close_dialog),
                ]
            )
            self.dialog.open()
        else:
            self.dialog = MDDialog(
                title=title,
                size_hint=(0.7, 1),
                text=text,
                buttons=[
                    MDRectangleFlatButton(
                        text='Close', on_release=self.close_dialog),
                ]
            )
            self.dialog.open()
