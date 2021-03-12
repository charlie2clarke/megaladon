from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem
from constants import ADDRESS_LABELS_DIR


class Dialog:
    def __init__(self):
        self._print_pdf = None

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def handle_item_click(self, item_clicked):
        self._print_pdf(item_clicked.text, ADDRESS_LABELS_DIR)

    def render_dialog(self, title, text, printers, print_pdf):
        if printers is not None:
            self._print_pdf = print_pdf
            dialog_items = [OneLineAvatarIconListItem(text=str(
                printer), on_release=self.handle_item_click) for printer in printers]
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
