'''Reusable component dialog component.

Dialog is a KivyMD component that could also be known as a modal
or popup.
'''
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem
from ...constants import ADDRESS_LABELS_DIR


class Dialog:
    '''KivyMD dialog component.

    Have separated use to increase cohesion, is likely that this
    would be reused by any future pages added to the app.

    Is implemented as a class because Kivy widgets require reference
    to instance variables.
    '''
    
    def __init__(self):
        '''Inits Dialog'''
        self._print_pdf = None

    def close_dialog(self, obj):
        '''Closes the popup to resume normal usage.'''
        self.dialog.dismiss()

    def handle_item_click(self, item_clicked):
        '''Handler for click of dialog items when printing.

        When dialog is used to render available printers, the
        user will select one, and the string of this is passed
        through here.

        Args:
            item_clicked: string of dialog item selected
                          (will be printer name).
        '''
        self._print_pdf(item_clicked.text, ADDRESS_LABELS_DIR)

    def render_dialog(self, title, text, printers, print_pdf):
        '''Opens a dialog with specific contents.

        If printers passed then will render a list of items showing
        all available printer for the user to select.

        Args:
            title: string of the title/header of dialog.
            text: string of body of the dialog. Cannot use body text
                  and dialog items - KivyMD limitation.
            printers: an array of strings with names of available printers.
            print_pdf: callback to function to print pdf file with selected
                       printer.
        '''
        if printers is not None:
            self._print_pdf = print_pdf
            dialog_items = [OneLineAvatarIconListItem(text=str(
                printer), on_release=self.handle_item_click) for
                printer in printers]
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
