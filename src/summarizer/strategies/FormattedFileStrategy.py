import io
import re
from abc import abstractmethod

import panflute
import pypandoc
import shutil
from kivy import Logger

from src.i18n.Translator import t as _
from src.summarizer.Summarizer import SummarizerStrategy
from src.utils.Docmdutils import parse_text, parse_paras


class FormattedFileStrategy(SummarizerStrategy):

    def __init__(self, path, loading_screen, lazy = False, generate_image = True):
        super().__init__(path, loading_screen, generate_image=generate_image)
        self.title = None
        self.lazy = lazy
        self.image_order = 0
        Logger.debug('Resbailing: Using FormattedFileStrategy')

    @staticmethod
    def check_input(values, **kwargs):
        order = kwargs.get('order', None)
        if order is None:
            return False

        if len(order) < 2:
            return False

        if order[0] != 1 or order[1] != 2:
            return False

        return values['title'] == 1 and values['section'] > 0



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
            elif isinstance(elem, panflute.Header) and elem.level == 2:
                last_header = elem
            elif isinstance(elem, panflute.Para):
                content = elem.content
                if len(content) > 0 and isinstance(content[0], panflute.Image):
                    image_path = content[0].url
                    self.copy_image(image_path)
                else:
                    paras[last_header] = paras.get(last_header, []) + [elem]
            elif isinstance(elem, panflute.Image):
                image_path = elem.url
                self.copy_image(image_path)
                # Copy the image to the output folder TODO: Make this work.
        return paras

    def copy_image(self, image_path):
        # The image path can be a relative path or an absolute path.
        # If it is a relative path, we need to get the absolute path.
        try:
            shutil.copyfile(image_path, self.writer.session_path + '/images/' + str(self.image_order) + '.png')
        except FileNotFoundError:
            match = re.search(r".*\\(.+)$", self.path)
            file_name = match.group(1)
            absolute_path = self.path[:-len(file_name)] + image_path
            shutil.copyfile(absolute_path, self.writer.session_path + '/images/image' + str(self.image_order) + '.png')
        finally:
            self.image_order += 1

    @abstractmethod
    def create_presentation(self, paras):
        if self.lazy:
            self.lazy_create_presentation(paras)
        else:
            self.smart_create_presentation(paras)

    def smart_create_presentation(self, paras):
        self.update_loading_info(_('loading.encoding_text'))
        parsed_paras = parse_paras(paras)
        slides =self.text_analyzer.populate_slides(parsed_paras)
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