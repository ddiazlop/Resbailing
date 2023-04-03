from src.summarizer.Summarizer import MarkdownSummarizerContext
from src.summarizer.strategies.FormattedFileStrategy import FormattedFileStrategy
from src.summarizer.strategies.NoFormatStrategy import NoFormatStrategy
from src.summarizer.strategies.TitleOnlyStrategy import TitleOnlyStrategy


def guess_summarization_strategy(path, loading_screen, lazy = False, generate_images = True):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()

        lines = text.splitlines()
        # Correctly formatted markdown files usually have a subheader as the second line
        if lines[1].startswith('##') and lines[0].startswith('#'):
            return MarkdownSummarizerContext(FormattedFileStrategy(path, loading_screen, lazy, generate_image=generate_images))
        elif lines[0].startswith('#'):
            return MarkdownSummarizerContext(TitleOnlyStrategy(path, loading_screen, generate_image=generate_images))
        else:
            return MarkdownSummarizerContext(NoFormatStrategy(path, loading_screen, generate_image=generate_images))