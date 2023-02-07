import panflute


def count_words(elem):
    return len([x for x in elem.content if isinstance(x, panflute.Space)])

def parse_text(elem):
    return ' '.join([x.text for x in elem.content if isinstance(x, panflute.Str)])

def new_slide(md_file, title):
    md_file.new_line('\n---\n')