from __tests__.mocks.views.LoadingScreenMock import LoadingScreenMock
from src.summarizer.strategies.AudioStrategy import AudioStrategy

from src.summarizer.strategies.FormattedFileStrategy import FormattedFileStrategy
from src.summarizer.strategies.NoFormatStrategy import NoFormatStrategy
from src.summarizer.strategies.TitleOnlyStrategy import TitleOnlyStrategy
from src.summarizer.strategies.utils.StrategyGuesser import guess_summarization_strategy2


class TestStrategyGuesser:
    """
    Tests that every summarization strategy is correctly guessed.
    """
    loading_screen = LoadingScreenMock()

    def test_formatted_file_strategy(self):
        """
        Tests that the FormattedFileStrategy is correctly guessed.
        :return:
        """
        guessed_strategy = guess_summarization_strategy2('tests/mocks/input/formatted_file.md', self.loading_screen)
        guessed_strategy.delete_output()
        assert guessed_strategy.strategy.__class__ == FormattedFileStrategy

    def test_title_only_strategy(self):
        """
        Tests that the TitleOnlyStrategy is correctly guessed.
        :return:
        """
        guessed_strategy = guess_summarization_strategy2('tests/mocks/input/title_only.md', self.loading_screen)
        guessed_strategy.delete_output()
        assert guessed_strategy.strategy.__class__ == TitleOnlyStrategy

    def test_no_format_strategy(self):
        """
        Tests that the NoFormatStrategy is correctly guessed.
        :return:
        """
        guessed_strategy = guess_summarization_strategy2('tests/mocks/input/no_format.md', self.loading_screen)
        guessed_strategy.delete_output()
        assert guessed_strategy.strategy.__class__ == NoFormatStrategy

    def test_audio_strategy(self):
        """
        Tests that the AudioStrategy is correctly guessed.
        :return:
        """
        guessed_strategy = guess_summarization_strategy2('tests/mocks/input/audio.mp3', self.loading_screen)
        guessed_strategy.delete_output()
        assert guessed_strategy.strategy.__class__ == AudioStrategy