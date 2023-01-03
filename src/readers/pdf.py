import PyPDF2


class DocumentData:
    def __init__(self, path):
        self.path = path
        pdf = PyPDF2.PdfReader(self.path)
        self.pages = pdf.pages

        # Data
        self.title = self.extract_title()
        i = 0

    def extract_title(self):
        def visitor_title(text, cm, tm, fontDict, fontSize):
            # TODO: Visitante que pueda extraer el título.
        first_page = self.pages[1]

