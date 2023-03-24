from abc import abstractmethod

import i18n
from kivy import Logger

from src.utils.Docmdutils import parse_text
from src.content_generators import SummarizerClass
from src.utils.TextAnalyzer import TextAnalyzer
from src.writers.MarkdownWriter import MarkdownWriter




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



class SummarizerStrategy:

    def __init__(self, path, loading_screen):
        self.update_loading_info = loading_screen.update_info
        self.update_loading_info(i18n.t('dict.loading_summarization_model'))
        self.writer = MarkdownWriter()
        self.summarizer = SummarizerClass(path)
        self.text_analyzer = TextAnalyzer()
        self.path = path

    def new_slide(self, header, para):
        self.writer.new_slide(header, self.summarizer.summarize_text(para))

    def parse_new_slide(self, header, para):
        header_parsed = parse_text(header)
        para_parsed = parse_text(para)
        self.new_slide(header_parsed, para_parsed)

    def summarize(self):
        Logger.debug('Resbailing: Summarizing ' + self.path)
        self.update_loading_info(i18n.t('dict.summarizing'))
        paras = self.init_content()
        self.create_presentation(paras)
        self.writer.create_file()

    @abstractmethod
    def init_content(self):
        pass

    @abstractmethod
    def create_presentation(self, paras):
        pass


