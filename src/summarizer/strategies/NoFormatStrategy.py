from kivy import Logger

from src.summarizer.strategies.TitleOnlyStrategy import TitleOnlyStrategy
from src.utils.text.TextCleaner import CleanerMethod
from src.i18n.Translator import t as _


class NoFormatStrategy(TitleOnlyStrategy):
    def __init__(self, path, loading_screen, generate_image: bool = True):
        super().__init__(path, loading_screen, generate_image)
        Logger.debug('Resbailing: Using NoFormatStrategy')

    @staticmethod
    def check_input(values, **kwargs):
        return values['title'] == 0 and values['section'] == 0 and values['images'] == 0

    def read_lines(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            full_text = f.read()
            return self.extract_sentences(full_text)

    def extract_sentences(self, full_text):
        # This is the only difference between this class and TitleOnlyStrategy
        cleaned_text = self.cleaner.clean_text(full_text.__str__(), CleanerMethod.ALL)
        title = self.summarizer.generate_title(cleaned_text)
        self.writer.write_header(title, 1)
        # End of difference
        lines = full_text.splitlines()
        lines = [line.strip() for line in lines]
        sentences = []
        self.update_loading_info(_('loading.analyzing_text'))
        for line in lines:
            line = self.cleaner.clean_text(line)
            line_sentences = self.text_analyzer.split_into_sentences(line)
            sentences.extend(line_sentences)
        return sentences
