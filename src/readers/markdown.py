import datetime
import io
import os

import i18n
import panflute
import pypandoc
from kivy import Logger
from mdutils import MdUtils

from src.utils.Docmdutils import count_words, parse_text
from src.utils.superclasses.content_generators import SummarizerClass, ImageGeneratorClass


class MarkdownSummarizer(SummarizerClass, ImageGeneratorClass):
    def __init__(self, path, loading_screen):
        self.update_loading_info = loading_screen.update_info
        today = datetime.date.today()
        # Create a folder for the session and its images
        session = "sessions/" + today.__str__()
        if not os.path.exists(session):
            os.mkdir(session)
            os.mkdir(session + "/images")
        self.session_path = session
        self.mdFile = MdUtils(file_name=self.session_path + "/presentation", title=today.__str__())
        super().__init__(path=path)

        self.update_loading_info(i18n.t('dict.loading_summarization_model'))

    def summarize(self):
        Logger.debug('src/readers/markdown.py: Summarizing ' + self.path)
        self.update_loading_info(i18n.t('dict.summarizing'))
        max_para_words, paras = self.init_content()
        # self.summarize_paras(max_para_words, paras)
        self.summarize_paras_lite(paras)
        self.mdFile.create_md_file()

    def summarize_paras_lite(self, paras):
        Logger.debug('src/readers/markdown.py: Summarizing paragraphs')
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

                    Logger.debug('src/readers/markdown.py: Summarizing paragraph ' + str(i + 1) + '->' + str(i+1+j) + '/' + str(
                            len(paras[header])) + ' of header ' + parse_text(header))
                    self.update_loading_info(i18n.t('dict.summarizing_paragraph') + ' ' + str(i + 1) + '->' + str(i+1+j) + '/' + str(
                            len(paras[header])) + ' ' + i18n.t('dict.of_header') + ' ' + parse_text(header))
                    self.new_slide(header, para)

            else:
                Logger.debug('src/readers/markdown.py: Summarizing paragraph 1/1 of header ' + parse_text(header))

                self.new_slide(header, paras[header][0])

    @staticmethod
    def extend_para(header, i, num_paras, para, paras):
        j = 0
        for j in range(int(num_paras / 5)):
            if len(paras[header]) > i + 1:
                next_para = paras[header][i + 1]
                para.content += next_para.content
                paras[header].remove(next_para)
        return j


    def new_slide(self, header, para):
        self.slide_break()
        self.mdFile.new_header(level=2, title=parse_text(header))
        summarized_text = self.summarize_text(parse_text(para))
        self.mdFile.new_paragraph(summarized_text)
        self.generate_image_to_mdfile(summarized_text)

    def slide_break(self):
        self.mdFile.new_line('\n---\n')

    def init_content(self):
        data = pypandoc.convert_file(self.path, 'json')
        doc = panflute.load(io.StringIO(data))
        paras = {}
        max_para_words = {}
        Logger.debug('src/readers/markdown.py: Getting titles and paragraphs')
        self.update_loading_info(i18n.t('dict.getting_titles_and_paragraphs'))
        for elem in doc.content:
            if isinstance(elem, panflute.Header) and elem.level == 1:
                self.title = parse_text(elem)
                self.mdFile.new_header(level=1, title=self.title)
                last_header = elem
            elif isinstance(elem, panflute.Header):
                last_header = elem
            elif isinstance(elem, panflute.Para):
                paras[last_header] = paras.get(last_header, []) + [elem]
                num_words = count_words(elem)
                if num_words > max_para_words.get(last_header, 0):
                    max_para_words[last_header] = num_words
        return max_para_words, paras
