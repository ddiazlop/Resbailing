import pytest

from __tests__.mocks.views.LoadingScreenMock import LoadingScreenMock
from src.summarizer.strategies.utils import StrategyGuesser

class TestSummarizer:
    """
    Tests that the summarizer works correctly.
    Takes a file that is a valid input and checks that it can give an output.
    """
    loading_screen = LoadingScreenMock()

    def test_no_format_e2e(self):
        summarizer = StrategyGuesser.guess_summarization_strategy2("tests/mocks/input/no_format.md", self.loading_screen, generate_images=False)
        try:
            summarizer.summarize()
            summarizer.delete_output()
        except Exception as e:
            pytest.fail(f"Summarization failed: {e}")

    def test_formatted_file_e2e(self):
        summarizer = StrategyGuesser.guess_summarization_strategy2("tests/mocks/input/formatted_file.md", self.loading_screen, generate_images=False)
        try:
            summarizer.summarize()
            summarizer.delete_output()
        except Exception as e:
            pytest.fail(f"Summarization failed: {e}")

    def test_title_only_e2e(self):
        summarizer = StrategyGuesser.guess_summarization_strategy2("tests/mocks/input/title_only.md", self.loading_screen, generate_images=False)
        try:
            summarizer.summarize()
            summarizer.delete_output()
        except Exception as e:
            pytest.fail(f"Summarization failed: {e}")

    def test_audio_e2e(self):
        summarizer = StrategyGuesser.guess_summarization_strategy2("tests/mocks/input/audio.mp3", self.loading_screen, generate_images=False)
        try:
            summarizer.summarize()
            summarizer.delete_output()
        except Exception as e:
            pytest.fail(f"Summarization failed: {e}")