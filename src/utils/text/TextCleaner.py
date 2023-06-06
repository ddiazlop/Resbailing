import re
from enum import Enum

import panflute


class CleanerMethod(Enum):
    MD = 1
    CITATIONS = 2
    ALL = 3

class TextCleaner:
    """A class that cleans text from unnecessary formatting and other stuff that is probably not relevant to the text."""
    def __init__(self):
        self.cleaning_methods = {
            CleanerMethod.MD : self.clean_md_text,
            CleanerMethod.CITATIONS : self.clean_citations,
            CleanerMethod.ALL : self.clean_all
        }

    @staticmethod
    def style_sentence(sentence : str) -> str:
        """
        Styles a sentence to be more readable. Lowercases everything, removes unnecessary spaces and adds a period at the end.
        Also capitalizes the first letter.
        :param sentence:
        :return:
        """
        sentence = sentence.lower()
        sentence = sentence.strip()
        if len(sentence) > 0:
            sentence = sentence[0].upper() + sentence[1:]
        if not sentence.endswith('.'):
            sentence += '.'
        return sentence

    @staticmethod
    def clean_md_text(text : str) -> str:
        """Removes all markdown formatting from the text."""
        text = panflute.convert_text(text, standalone=True, input_format='markdown', output_format='plain')
        return text.strip()

    @staticmethod
    def clean_citations(text : str) -> str:
        """Removes all citations from the text. Given that it appears as [1] or [1,2]"""
        text = re.sub(r'\[\d+(,\d+)*\]', '', text)
        return text.strip()

    @staticmethod
    def check_spam(text : str) -> bool:
        """Checks if the text is spam."""
        if text.__contains__('CNN'):
            return True
        if text.__contains__('Sportsmail.com'):
            return True
        return False

    def clean_all(self, text : str) -> str:
        """Removes all formatting from the text."""
        return self.clean_citations(self.clean_md_text(text))

    def clean_text(self, text : str, method: [CleanerMethod] = None) -> str:
        """Removes unnecessary formatting from the text. And also revomeves everything that is probably not relevant to the text."""
        if method is None:
            method = [CleanerMethod.ALL]

        if not isinstance(method, list):
            method = [method]

        for m in method:
            text = self.cleaning_methods[m](text)
        return text