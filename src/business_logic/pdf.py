from fpdf import FPDF


class Pdf:
    def __init__(self):
        self.document = FPDF(format='A4', orientation='L', unit='in')
        self.document.add_page()
        self.document.set_font('Arial', '', 14)
        self.effective_width = self.document.w - 2 * self.document.l_margin
        self.column_width = self.effective_width / 6

    def write_pdf(self, data):
        # product id, aisle, shelf, description, quantity, space for tick
        self.document.set_font('Arial', 'B', 18)
        self.document.cell(self.effective_width, 0.0,
                           'Picking List', align='C')
        self.document.set_font('Arial', '', 12)
        self.document.ln(0.5)
        self.text_height = self.document.font_size

        for index, row in enumerate(data):
            if index == 0:
                self.document.set_font('Arial', 'B', 12)
                self.document.set_fill_color(230, 230, 230)
            else:
                self.document.set_font('Arial', '', 10)
                self.document.set_fill_color(255, 255, 255)
            for item in row:
                self.document.cell(
                    self.column_width, 2 * self.text_height, str(item), border=1, fill=True)
            self.document.ln(self.text_height * 2)

        self.document.output('test_pdf.pdf')
