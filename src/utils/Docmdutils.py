import panflute


def count_words(elem):
    return len([x for x in elem.content if isinstance(x, panflute.Str)])


def parse_text(elem):
    result = ''
    for x in elem.content:
        if isinstance(x, panflute.Str):
            result += x.text
        elif isinstance(x, panflute.Space):
            result += ' '
        elif isinstance(x, panflute.Quoted):
            result += '"' + parse_text(x) + '"'
    return result
