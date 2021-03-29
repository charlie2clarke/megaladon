'''Creates PDF files.

Writes 3 different types of PDFs:
1. Picking list
2. Packaging list
3. Address label
'''
from fpdf import FPDF
from .constants import SENDER_DETAILS


class Pdf:
    '''Uses FPDF library to create PDF files.'''

    def __init__(self):
        self._document = None
        self._effective_width = None
        self._column_width = None
        self._text_height = None

    def _create_page(self):
        # Initialising here rather than in constructor because some methods
        # are invoked iteratively, so need to create a new page each time.
        self._document = FPDF(format='A4', orientation='L', unit='in')
        self._document.add_page()
        self._document.set_font('Arial', '', 14)
        self._effective_width = self._document.w - 2 * self._document.l_margin
        self._column_width = self._effective_width / 6
        self._text_height = self._document.font_size

    def _set_text_style(self, index):
        # Sets font and size. Sets to bold if index
        # is 0 for heading style.
        if index == 0:
            self._document.set_font('Arial', 'B', 11)
            self._document.set_fill_color(230, 230, 230)
        else:
            self._document.set_font('Arial', '', 10)
            self._document.set_fill_color(255, 255, 255)

    def _create_table(self, data):
        for index, row in enumerate(data):
            self._set_text_style(index)
            for item in row:
                item = str(item)
                # Styling for header row.
                if index == 0:
                    item.replace('_', ' ')
                    item.capitalize()
                self._document.cell(
                    self._column_width, 2 * self._text_height, str(item),
                    border=1, fill=True)
            self._document.ln(self._text_height * 2)

    def write_picking_list(self, data, destination):
        '''Creates a PDF file with a table of all data passed.

        Args:
            data: a list with a list for each row to be written
            (all items strings).
            destination: folder path to write file to.

        Raises:
            Exception: an error in outputting the file.
        '''
        self._create_page()
        # Writing title.
        self._document.set_font('Arial', 'B', 18)
        self._document.cell(self._effective_width, 0.0,
                            'Picking List', align='C')

        self._document.set_font('Arial', '', 12)
        self._document.ln(0.5)
        self._create_table(data)
        file_name = destination + '/Picking List.pdf'
        try:
            self._document.output(name=file_name, dest='F')
        except Exception as e:
            print("There was an error - have you already got a file called"
                  " Picking List.pdf open?")

    def write_packaging_list(
        self,
        date,
        address,
        items,
        order_id,
        destination
    ):
        '''Creates PDF file with:
        Sender address
        Customer address
        Table of ordered items

        Args:
            date: string of order date.
            address: a list of address details with a list for each line.
            items:  a list of items and quantities with a list for each item.
            order_id: integer id of order.
            destination: folder path to write files to.
        '''
        self._create_page()
        self._document.set_x(-30)

        # Write sender details.
        for index, item in enumerate(SENDER_DETAILS):
            self._set_text_style(index)
            self._document.cell(
                self._column_width, 2 * self._text_height, str(item), border=0)
            self._document.ln(self._text_height * 1.5)

        # Write invoice number and order date.
        self._document.ln(0.5)
        self._document.cell(
            self._column_width, 2 * self._text_height, 'Invoice No. xxxxxxxx"\
            "                                             Date: ' + date,
            border=0)
        self._document.ln(0.5)

        # Write customer address.
        for index, item in enumerate(address):
            self._set_text_style(index)
            self._document.cell(
                self._column_width, 2 * self._text_height, str(item), border=0)
            self._document.ln(self._text_height * 1.5)

        # Write table of ordered items.
        self._document.set_font('Arial', '', 12)
        self._document.ln(self._text_height * 2.5)
        self._create_table(items)

        file_name = destination + '/Packaging List ' + \
            address[1] + ' ' + str(order_id) + '.pdf'
        self._document.output(name=file_name, dest='F')

    def write_address_label(self, address, order_id, destination):
        '''Write PDF file containing customer name and address.

        Args:
            address: a list of address details with list for each line.
            order_id: integer id of order.
            destination: folder path to write file to.
        '''
        self._create_page()

        for item in address:
            self._document.cell(
                self._column_width, 2 * self._text_height, str(item), border=0)
            self._document.ln(self._text_height * 1.5)

        file_name = destination + '/Address Label ' + \
            address[0] + ' ' + str(order_id) + '.pdf'
        self._document.output(name=file_name, dest='F')
