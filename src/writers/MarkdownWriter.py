import datetime
import os
import random
import shutil

from mdutils import MdUtils

from src.content_generators import  ImageGeneratorClass
from src.utils.Docmdutils import parse_text


class MarkdownWriter:
    def __init__(self):

        today = datetime.date.today()
        session = "sessions/" + today.__str__()

        while os.path.exists(session):
            if session.__contains__("_"):
                session = session + random.randint(0, 10).__str__()
            else:
                session = session + "_" + random.randint(0, 10).__str__()

        self.session_path = session
        self.images_dir = session + "/images"
        self.audio_dir = session + "/audio"

        os.mkdir(session)
        os.mkdir(self.images_dir)
        os.mkdir(self.audio_dir)


        self.image_generator = ImageGeneratorClass()
        self.md_file = MdUtils(file_name=self.session_path + "/presentation", title=today.__str__())
        self.slide_count = 0
        self.pregenerated_images = []

    def create_file(self):
        self.md_file.create_md_file()

    def delete_session(self):
        shutil.rmtree(self.session_path)

    def new_slide(self, header, para, generate_image : bool=True) -> None:
        if self.slide_count == 0:
            self.get_pregenerated_images()

        self.slide_break()
        self.write_header(header)
        self.write_paragraph(para)

        if self.slide_count < len(self.pregenerated_images):
            self.image_generator.place_image_to_mdfile(self.pregenerated_images[self.slide_count], self.session_path, self.md_file)
        elif generate_image:
            self.image_generator.generate_image_to_mdfile(header, self.md_file, self.session_path, self.slide_count)

        self.slide_count += 1

    def get_pregenerated_images(self):
        # Look for already existing images
        files = os.listdir(self.images_dir)
        for file in files:
            if file.startswith("image"):
                self.pregenerated_images.append(file)

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
