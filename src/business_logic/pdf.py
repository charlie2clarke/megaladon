from fpdf import FPDF

class Pdf:
    def __init__(self):
        self.document = FPDF()

    def write_pdf(self):
        self.document.add_page()
        self.document.output('test_pdf.pdf')