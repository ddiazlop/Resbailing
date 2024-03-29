from src.summarizer.Summarizer import MarkdownSummarizerContext
from src.summarizer.strategies.AudioStrategy import AudioStrategy
from src.summarizer.strategies.FormattedFileStrategy import FormattedFileStrategy
from src.summarizer.strategies.NoFormatStrategy import NoFormatStrategy
from src.summarizer.strategies.TitleOnlyStrategy import TitleOnlyStrategy


### This is the old guesser, it is not used anymore, but it is kept for reference
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


def guess_summarization_strategy2(path, loading_screen, lazy = False, generate_images = True) -> MarkdownSummarizerContext:
    """
    Guesses the summarization strategy to use based on the file format.
    Uses a simple heuristic to determine the strategy to use.
    :param path:
    :param loading_screen:
    :param lazy:
    :param generate_images:
    :return:
    """

    values = {'title': 0, 'section': 0, 'images': 0, 'bodies': 0}
    order = []

    # AudioStrategy
    if AudioStrategy.check_input(values, filename=path):
        return MarkdownSummarizerContext(AudioStrategy(path, loading_screen, generate_image=generate_images))


    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines: # This is a very naive approach, there's probably a better way to do this
            if line.startswith('##'):
                values['section'] += 1
                order.append(2)
            elif line.startswith('#'):
                values['title'] += 1
                order.append(1)
            elif line.startswith('!['):
                values['images'] += 1
                order.append('Image')
            elif not line.isspace():
                values['bodies'] += 1
                order.append('Body')

        if values['bodies'] != values['section'] and values['section'] > 0:
            raise ValueError('The number of bodies and sections do not match')

        # FormattedFileStrategy
        if FormattedFileStrategy.check_input(values, order = order):
            return MarkdownSummarizerContext(FormattedFileStrategy(path, loading_screen, lazy, generate_image=generate_images))

        # TitleOnlyStrategy
        if TitleOnlyStrategy.check_input(values, order = order):
            return MarkdownSummarizerContext(TitleOnlyStrategy(path, loading_screen, generate_image=generate_images))

        # NoFormatStrategy
        if NoFormatStrategy.check_input(values, order = order):
            return MarkdownSummarizerContext(NoFormatStrategy(path, loading_screen, generate_image=generate_images))

        raise NotImplementedError('Could not find the summarization strategy to use')


