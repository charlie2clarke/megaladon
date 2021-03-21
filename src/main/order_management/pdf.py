from fpdf import FPDF
from .constants import SENDER_DETAILS


class Pdf:

    def _create_page(self):
        # Initialising here rather than in constructor because some methods are invoked
        # iteratively, so need to create a new page each time.
        self._document = FPDF(format='A4', orientation='L', unit='in')
        self._document.add_page()
        self._document.set_font('Arial', '', 14)
        self._effective_width = self._document.w - 2 * self._document.l_margin
        self._column_width = self._effective_width / 6
        self._text_height = self._document.font_size

    def _set_text_style(self, index):
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
                if index == 0:
                    item.replace('_', ' ')
                    item.capitalize()
                self._document.cell(
                    self._column_width, 2 * self._text_height, str(item), border=1, fill=True)
            self._document.ln(self._text_height * 2)

    def write_picking_list(self, data, destination):
        self._create_page()
        # product id, aisle, shelf, description, quantity, space for tick

        # Writing title
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
            print("There was an error - have you already got a file called Picking List.pdf open?")

    def write_packaging_list(self, date, address, items, order_id, destination):
        self._create_page()
        self._document.set_x(-30)

        for index, item in enumerate(SENDER_DETAILS):
            self._set_text_style(index)
            self._document.cell(
                self._column_width, 2 * self._text_height, str(item), border=0)
            self._document.ln(self._text_height * 1.5)

        self._document.ln(0.5)
        self._document.cell(
            self._column_width, 2 * self._text_height, 'Invoice No. xxxxxxxx                                             Date: ' + date, border=0)
        self._document.ln(0.5)

        for index, item in enumerate(address):
            self._set_text_style(index)
            self._document.cell(
                self._column_width, 2 * self._text_height, str(item), border=0)
            self._document.ln(self._text_height * 1.5)

        self._document.set_font('Arial', '', 12)
        self._document.ln(self._text_height * 2.5)
        self._create_table(items)

        file_name = destination + '/Packaging List ' + \
            address[1] + ' ' + str(order_id) + '.pdf'
        self._document.output(name=file_name, dest='F')


    def write_address_label(self, address, order_id, destination):
        self._create_page()

        for item in address:
            self._document.cell(
                self._column_width, 2 * self._text_height, str(item), border=0)
            self._document.ln(self._text_height * 1.5)

        file_name = destination + '/Address Label ' + \
            address[0] + ' ' + str(order_id) + '.pdf'
        self._document.output(name=file_name, dest='F')
