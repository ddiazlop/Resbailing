from kivy import Logger

from AppConfig import app_config
from src.summarizer.Summarizer import SummarizerStrategy
from src.utils.text.TextCleaner import CleanerMethod
from src.i18n.Translator import t as _


class TitleOnlyStrategy(SummarizerStrategy):

    @staticmethod
    def check_input(values, **kwargs):
        order = kwargs.get('order', None)
        if order is None or len(order) < 1:
            return False
        if order[0] != 1:
            return False

        return values['title'] == 1 and values['section'] == 0 and values['images'] == 0

    def __init__(self, path, loading_screen, generate_image=True):
        super().__init__(path, loading_screen, generate_image=generate_image)
        Logger.debug('Resbailing: Using TitleOnlyStrategy')

    def read_lines(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.title = self.cleaner.clean_text(lines[0], CleanerMethod.MD)
            self.writer.write_header(self.title, 1)

            lines = [line.strip() for line in lines[1:]]
            sentences = []

            self.update_loading_info(_('loading.analyzing_text'))
            for line in lines:
                line = self.cleaner.clean_text(line)
                line_sentences = self.text_analyzer.split_into_sentences(line)
                sentences.extend(line_sentences)
            return sentences

    def init_content(self):
        paras = {}
        sentences = self.read_lines()

        # Merging sentences that are similiar to each other.
        merged_senteces = self.text_analyzer.get_merged_sentences(sentences)
        if app_config.debug:
            for sentence in merged_senteces:
                Logger.debug('Resbailing: Merged sentence ' + str(merged_senteces.index(sentence) + 1)+'/' + str(len(merged_senteces))  + ': ' + sentence)

        # This way we can guess the titles for each slide.
        for sentence in merged_senteces:
            self.update_loading_info(_('loading.creating_titles') + ' ' + str(merged_senteces.index(sentence) + 1) + '/' + str(len(merged_senteces)))
            really_summarized = self.summarizer.generate_title(sentence)
            if really_summarized not in paras:
                paras[really_summarized] = [sentence]
            else:
                paras[really_summarized].append(sentence)

        return paras

    def create_presentation(self, paras) -> None:
        self.generate_slides(paras)

