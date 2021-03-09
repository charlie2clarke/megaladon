import win32api
import win32print
from pathlib import Path
import os
from constants import ADDRESS_LABELS_DIR

class Print:
    all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]

    @staticmethod
    def print_pdf(selected_printer, directory_name):
        def get_printer_index(selected_printer):
            for index, printer_details in enumerate(win32print.EnumPrinters(2)):
                if printer_details[2] == selected_printer:
                    return index

        printer_num = get_printer_index(selected_printer)

        win32print.SetDefaultPrinter(Print.all_printers[printer_num])

        for path in Path(ADDRESS_LABELS_DIR).rglob('*.pdf'):
            try:
                win32api.ShellExecute(0, 'print', str(path), None, '.', 0)
            except:
                print("There was a problem with the selected printer - this might be because you don't have a default pdf reader in your system settings")


