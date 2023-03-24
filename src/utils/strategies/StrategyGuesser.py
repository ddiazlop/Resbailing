from src.summarizer.Summarizer import MarkdownSummarizerContext
from src.summarizer.strategies.FormattedFileStrategy import FormattedFileStrategy


def guess_summarization_strategy(path, loading_screen, lazy = False):
    with open(path, 'r') as file:
        text = file.read()

        lines = text.splitlines()
        # Correctly formatted markdown files usually have a subheader as the second line
        if lines[1].startswith('##'):
            return MarkdownSummarizerContext(FormattedFileStrategy(path, loading_screen, lazy))
        # elif lines[0].startswith('#'):
        #     return MarkdownSummarizerContext(Divi(path, loading_screen))