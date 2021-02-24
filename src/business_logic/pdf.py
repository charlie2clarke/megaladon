from fpdf import FPDF

class Pdf:
    def __init__(self):
        self.document = FPDF()
        self.document.add_page()
        self.document.set_font('Arial', '', 14)

    def write_pdf(self, data):
        # product id, aisle, shelf, description, quantity, space for tick
        for item in data:
            self.document.write(5, str(item))
        self.document.output('test_pdf.pdf')