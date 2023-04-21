import pytest
import app_config

from src.summarizer.strategies.FormattedFileStrategy import FormattedFileStrategy
from src.summarizer.strategies.NoFormatStrategy import NoFormatStrategy
from src.summarizer.strategies.TitleOnlyStrategy import TitleOnlyStrategy
from src.summarizer.strategies.utils.StrategyGuesser import guess_summarization_strategy2
from tests.mocks.views.LoadingScreenMock import LoadingScreenMock


class TestStrategyGuesser:
    """
    Tests that every summarization strategy is correctly guessed.
    """
    loading_screen = LoadingScreenMock()

    def test_formattedfilestrategy(self):
        """
        Tests that the FormattedFileStrategy is correctly guessed.
        :return:
        """
        guessed_strategy = guess_summarization_strategy2('tests/mocks/formatted_file.md', self.loading_screen)
        assert guessed_strategy.strategy.__class__ == FormattedFileStrategy

    def test_titleonlystrategy(self):
        """
        Tests that the TitleOnlyStrategy is correctly guessed.
        :return:
        """
        guessed_strategy = guess_summarization_strategy2('tests/mocks/input/title_only.md', self.loading_screen)
        assert guessed_strategy.strategy.__class__ == TitleOnlyStrategy

    def test_noformatstrategy(self):
        """
        Tests that the NoFormatStrategy is correctly guessed.
        :return:
        """
        guessed_strategy = guess_summarization_strategy2('tests/mocks/input/no_format.md', self.loading_screen)
        assert guessed_strategy.strategy.__class__ == NoFormatStrategy


