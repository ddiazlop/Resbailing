import io
from abc import abstractmethod

import panflute
import pypandoc
from kivy import Logger

from src.i18n.Translator import t as _
from src.summarizer.Summarizer import SummarizerStrategy
from src.utils.Docmdutils import parse_text, parse_paras


class FormattedFileStrategy(SummarizerStrategy):

    def __init__(self, path, loading_screen, lazy = False, generate_image = True):
        super().__init__(path, loading_screen, generate_image=generate_image)
        self.title = None
        self.lazy = lazy
        Logger.debug('Resbailing: Using FormattedFileStrategy')


    def init_content(self):
        last_header = None
        data = pypandoc.convert_file(self.path, 'json')
        doc = panflute.load(io.StringIO(data))
        paras = {}
        Logger.debug('Resbailing: Getting titles and paragraphs')
        self.update_loading_info(_('loading.getting_titles_and_paragraphs'))
        for elem in doc.content:
            if isinstance(elem, panflute.Header) and elem.level == 1:
                self.title = parse_text(elem)
                self.writer.write_header(self.title, 1)
                last_header = elem
            elif isinstance(elem, panflute.Header):
                last_header = elem
            elif isinstance(elem, panflute.Para):
                paras[last_header] = paras.get(last_header, []) + [elem]
        return paras

    @abstractmethod
    def create_presentation(self, paras):
        if self.lazy:
            self.lazy_create_presentation(paras)
        else:
            self.smart_create_presentation(paras)

    def smart_create_presentation(self, paras):
        self.update_loading_info(_('dict.encoding_text'))
        parsed_paras = parse_paras(paras)
        self.text_analyzer.populate_slides(parsed_paras)
        slides = self.text_analyzer.slides

        self.generate_slides(slides)

    def lazy_create_presentation(self, paras):
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

                    Logger.debug('Resbailing: Summarizing paragraph ' + str(i + 1) + '->' + str(i + 1 + j) + '/' + str(
                        len(paras[header])) + ' of header ' + parse_text(header))
                    self.update_loading_info(
                        _('loading.summarizing_paragraph') + ' ' + str(i + 1) + '->' + str(i + 1 + j) + '/' + str(
                            len(paras[header])) + ' ' + _('loading.of_header') + ' ' + parse_text(header))
                    self.parse_new_slide(header, para)

            else:
                Logger.debug('Resbailing: Summarizing paragraph 1/1 of header ' + parse_text(header))
                self.parse_new_slide(header, paras[header][0])

    @staticmethod
    def extend_para(header, i, num_paras, para, paras):
        j = 0
        for j in range(int(num_paras / 5)):
            if len(paras[header]) > i + 1:
                next_para = paras[header][i + 1]
                para.content += next_para.content
                paras[header].remove(next_para)
        return j