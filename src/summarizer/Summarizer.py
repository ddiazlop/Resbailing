from abc import abstractmethod
from typing import Dict, List

from kivy import Logger

from src.utils.Docmdutils import parse_text
from src.content_generators import SummarizerClass
from src.utils.text.TextAnalyzer import TextAnalyzer, ThresholdMode
from src.utils.text.TextCleaner import TextCleaner
from src.utils.MarkdownWriter import MarkdownWriter
from src.i18n.Translator import t as _




class MarkdownSummarizerContext:
    def __init__(self, summarizer_strategy):
        self._strategy = summarizer_strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy) -> None:
        self._strategy = strategy

    def summarize(self):
        self._strategy.summarize()

    def delete_output(self):
        self._strategy.delete_output()



class SummarizerStrategy:

    def __init__(self, path, loading_screen, generate_image : bool=True):
        self.update_loading_info = loading_screen.update_info
        self.update_loading_info(_('loading.loading_summarization_model'))
        self.writer = MarkdownWriter()
        self.summarizer = SummarizerClass(path)
        self.text_analyzer = TextAnalyzer(ThresholdMode.MEDIAN)
        self.cleaner = TextCleaner()
        self.path = path
        self.generate_image = generate_image
        self.title = None

    def new_slide(self, header, para):
        if len(para) > self.summarizer.max_length:
            summarized_para = self.summarizer.summarize_text(para)
        else:
            summarized_para = para
        if not self.cleaner.check_spam(header) and not self.cleaner.check_spam(summarized_para):
            self.writer.new_slide(header, summarized_para, generate_image=self.generate_image)

    def parse_new_slide(self, header, para):
        header_parsed = parse_text(header)
        para_parsed = parse_text(para)
        self.new_slide(header_parsed, para_parsed)

    def summarize(self):
        Logger.debug('Resbailing: Summarizing ' + self.path)
        self.update_loading_info(_('loading.summarizing'))
        paras = self.init_content()

        self.update_loading_info(_('loading.getting_background_image'))
        if self.generate_image:
            self.writer.image_generator.generate_background_image(self.title, self.writer.session_path)

        self.update_loading_info(_('loading.generating_slides'))
        self.create_presentation(paras)
        self.writer.create_file()

    def generate_slides(self, slides : Dict[str, List[str]]) -> None:
        """
        Generates slides from a dictionary of headers and paragraphs and writes them to the md file

        :param slides:  A dictionary of headers and paragraphs to be written to the md file
        """
        for header, paras in slides.items():
            if not header.__contains__('CNN'):
                for para in paras:
                    self.update_loading_info(
                        _('loading.summarizing_paragraph') + ' ' + str(paras.index(para) + 1) + '/' + str(
                                len(paras)) + ' ' + _('loading.of_header') + ' ' + header)
                    self.new_slide(header, para)

    def delete_output(self):
        self.writer.delete_session()

    @abstractmethod
    def init_content(self):
        pass

    @abstractmethod
    def create_presentation(self, paras):
        pass

    @staticmethod
    @abstractmethod
    def check_input(values, **kwargs):
        pass

