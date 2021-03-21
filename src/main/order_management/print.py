'''Allows printing of files on Windows systems.

Gets all printers listed on user's Windows system and prints all PDF
files within a given directory.
'''
import win32api
import win32print
from pathlib import Path


class Print:
    '''Prints files on a Windows PC.

    Attributes:
        all_printers: a list of available printer names.
    '''

    all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]

    def print_pdf(selected_printer, destination):
        '''Prints all PDF files within a given directory using a selected
        printer.

        Args:
            selected_printer: a string of the printer wanting to use.
            destination: folder path to search for PDF files to print.

        Raises:
            Exception: an error occuring when executing print.
        '''
        def get_printer_index(selected_printer):
            # Finds the index of the printer by the printer name.
            for index, printer_details in enumerate(
             win32print.EnumPrinters(2)):
                if printer_details[2] == selected_printer:
                    return index

        printer_num = get_printer_index(selected_printer)

        win32print.SetDefaultPrinter(Print.all_printers[printer_num])

        for path in Path(destination).rglob('*.pdf'):
            try:
                win32api.ShellExecute(0, 'print', str(path), None, '.', 0)
            except Exception as e:
                print("There was a problem with the selected printer - this "
                      "might be because you don't have a default pdf reader in"
                      " your system settings. More details: " + str(e))
                raise
