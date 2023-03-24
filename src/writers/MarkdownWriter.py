import datetime
import os

from mdutils import MdUtils

from src.content_generators import  ImageGeneratorClass
from src.utils.Docmdutils import parse_text


class MarkdownWriter:
    def __init__(self):

        today = datetime.date.today()
        session = "sessions/" + today.__str__()

        if not os.path.exists(session):
            os.mkdir(session)
            os.mkdir(session + "/images")

        self.session_path = session
        self.image_generator = ImageGeneratorClass()
        self.md_file = MdUtils(file_name=self.session_path + "/presentation", title=today.__str__())

    def create_file(self):
        self.md_file.create_md_file()

    def new_slide(self, header, para):
        self.slide_break()
        self.write_header(header)
        self.write_paragraph(para)
        self.image_generator.generate_image_to_mdfile(para, self.md_file, self.session_path)

    def parse_new_slide(self, header, para):
        header_parsed = parse_text(header)
        para_parsed = parse_text(para)
        self.new_slide(header_parsed, para_parsed)

    def slide_break(self):
        self.md_file.new_line('\n---\n')

    def write_header(self, header, level=2):
        self.md_file.new_header(level=level, title=header)

    def write_paragraph(self, para):
        self.md_file.new_paragraph(para)
