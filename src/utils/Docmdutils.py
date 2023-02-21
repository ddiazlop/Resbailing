import panflute


def count_words(elem):
    return len([x for x in elem.content if isinstance(x, panflute.Str)])

def parse_text(elem):
    return ' '.join([x.text for x in elem.content if isinstance(x, panflute.Str)])