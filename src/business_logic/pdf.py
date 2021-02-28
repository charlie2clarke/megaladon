from fpdf import FPDF
# from presentation.order_management.order_management_view import OrderManagementScreen


class Pdf:
    # def __init__(self):
    #     # self.order_management_view = OrderManagementScreen()
        
    def create_page(self):
        self.document = FPDF(format='A4', orientation='L', unit='in')
        self.document.add_page()
        self.document.set_font('Arial', '', 14)
        self.effective_width = self.document.w - 2 * self.document.l_margin
        self.column_width = self.effective_width / 6
        self.text_height = self.document.font_size

    def set_text_style(self, index):
        if index == 0:
            self.document.set_font('Arial', 'B', 11)
            self.document.set_fill_color(230, 230, 230)
        else:
            self.document.set_font('Arial', '', 10)
            self.document.set_fill_color(255, 255, 255)

    def create_table(self, data):
        for index, row in enumerate(data):
            self.set_text_style(index)
            for item in row:
                item = str(item)
                if index == 0:
                    item.replace('_', ' ')
                    item.capitalize()
                self.document.cell(
                    self.column_width, 2 * self.text_height, str(item), border=1, fill=True)
            self.document.ln(self.text_height * 2)

    def write_picking_list(self, data):
        self.create_page()
        # product id, aisle, shelf, description, quantity, space for tick

        # Writing title
        self.document.set_font('Arial', 'B', 18)
        self.document.cell(self.effective_width, 0.0,
                           'Picking List', align='C')
        self.document.set_font('Arial', '', 12)
        self.document.ln(0.5)

        self.create_table(data)

        self.document.output(name='Picking List.pdf')
        # self.order_management_view.render_dialog('Picking List Successfully Created!', 'You can find the pdf document in the root of directory of this project')

    def write_packaging_list(self, date, address, items, number):
        self.create_page()
        sender_details = ['Sender:', 'Awesome Organisation Inc.',
                          'Building Abbey Road', 'London', 'L2C 802', '12345 678910']

        self.document.set_x(-30)
        for index, item in enumerate(sender_details):
            self.set_text_style(index)
            self.document.cell(
                self.column_width, 2 * self.text_height, str(item), border=0)
            self.document.ln(self.text_height * 1.5)
        
        self.document.ln(0.5)
        self.document.cell(
            self.column_width, 2 * self.text_height, 'Invoice No. xxxxxxxx                                             Date: ' + date, border=0)

        self.document.ln(0.5)
        
        
        for index, item in enumerate(address):
            self.set_text_style(index)
            self.document.cell(
                self.column_width, 2 * self.text_height, str(item), border=0)
            self.document.ln(self.text_height * 1.5)
        self.document.set_font('Arial', '', 12)
        self.document.ln(self.text_height * 2.5)
        self.create_table(items)

        self.document.output(name='Packaging List ' + address[1] + ' ' + str(number) + '.pdf')

