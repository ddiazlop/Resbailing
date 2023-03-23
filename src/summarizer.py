import datetime
import io
import os

import i18n
import numpy
import panflute
import pypandoc
import torch
from kivy import Logger
from mdutils import MdUtils
from transformers import AutoTokenizer, AutoModel

import torch.nn.functional as F
from src.utils.Docmdutils import count_words, parse_text, parse_paras
from src.content_generators import SummarizerClass, ImageGeneratorClass
from src.utils.TextAnalyzer import TextAnalyzer


class MarkdownWriter:
    def __init__(self):

        today = datetime.date.today()
        session = "sessions/" + today.__str__()

        if not os.path.exists(session):
            os.mkdir(session)
            os.mkdir(session + "/images")

        self.session_path = session
        self.summarizer = SummarizerClass(session)
        self.image_generator = ImageGeneratorClass()
        self.md_file = MdUtils(file_name=self.session_path + "/presentation", title=today.__str__())

    def create_file(self):
        self.md_file.create_md_file()

    def new_slide(self, header, para):
        self.slide_break()
        self.write_header(header)
        summarized_text = self.summarizer.summarize_text(para)
        self.write_paragraph(summarized_text)
        self.image_generator.generate_image_to_mdfile(summarized_text, self.md_file, self.session_path)

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


class MarkdownSummarizer(SummarizerClass, ImageGeneratorClass):
    def __init__(self, path, loading_screen):
        self.writer = MarkdownWriter()
        self.text_analyzer = TextAnalyzer();
        self.update_loading_info = loading_screen.update_info
        self.update_loading_info(i18n.t('dict.loading_summarization_model'))
        super().__init__(path=path)


    def summarize(self):
        Logger.debug('Resbailing: Summarizing ' + self.path)
        self.update_loading_info(i18n.t('dict.summarizing'))
        max_para_words, paras = self.init_content()
        self.get_paras_corr(paras)
        # self.summarize_paras_lazy(paras)
        self.writer.create_file()



    def get_paras_corr(self, paras):
        self.update_loading_info(i18n.t('dict.encoding_text'))
        parsed_paras = parse_paras(paras)

        self.text_analyzer.populate_slides(parsed_paras)
        slides = self.text_analyzer.slides

        for header, paras in slides.items():
            for para in paras:
                self.update_loading_info(i18n.t('dict.summarizing_paragraph') + ' ' + str(paras.index(para) + 1) + '/' + str(
                    len(paras)) + ' ' + i18n.t('dict.of_header') + ' ' + header)
                self.writer.new_slide(header, para)





    def summarize_paras_lazy(self, paras):
        Logger.debug('Resbailing: Summarizing paragraphs')
        for header in paras.keys():
            num_paras = len(paras[header])
            if num_paras > 1:
                for i in range(len(paras[header])):
                    if i >= len(paras[header]):
                        break
                    if i < len(paras[header]):
                        para = paras[header][i]
                        # Extend the paragraph to make it longer
                        j = self.extend_para(header, i, num_paras, para, paras)

                    Logger.debug('Resbailing: Summarizing paragraph ' + str(i + 1) + '->' + str(i+1+j) + '/' + str(
                            len(paras[header])) + ' of header ' + parse_text(header))
                    self.update_loading_info(i18n.t('dict.summarizing_paragraph') + ' ' + str(i + 1) + '->' + str(i+1+j) + '/' + str(
                            len(paras[header])) + ' ' + i18n.t('dict.of_header') + ' ' + parse_text(header))
                    self.writer.parse_new_slide(header, para)

            else:
                Logger.debug('Resbailing: Summarizing paragraph 1/1 of header ' + parse_text(header))

                self.writer.parse_new_slide(header, paras[header][0])

    @staticmethod
    def extend_para(header, i, num_paras, para, paras):
        j = 0
        for j in range(int(num_paras / 5)):
            if len(paras[header]) > i + 1:
                next_para = paras[header][i + 1]
                para.content += next_para.content
                paras[header].remove(next_para)
        return j

    def init_content(self):
        last_header = None
        data = pypandoc.convert_file(self.path, 'json')
        doc = panflute.load(io.StringIO(data))
        paras = {}
        max_para_words = {}
        Logger.debug('Resbailing: Getting titles and paragraphs')
        self.update_loading_info(i18n.t('dict.getting_titles_and_paragraphs'))
        for elem in doc.content:
            if isinstance(elem, panflute.Header) and elem.level == 1:
                self.title = parse_text(elem)
                self.writer.write_header(self.title, 1)
                last_header = elem
            elif isinstance(elem, panflute.Header):
                last_header = elem
            elif isinstance(elem, panflute.Para):
                paras[last_header] = paras.get(last_header, []) + [elem]
                num_words = count_words(elem)
                if num_words > max_para_words.get(last_header, 0):
                    max_para_words[last_header] = num_words
        return max_para_words, paras
