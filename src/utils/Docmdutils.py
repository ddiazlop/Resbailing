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

def parse_paras(paras):
        parsed_paras = {}
        for header in paras:
            parsed_header = parse_text(header)
            for para in paras[header]:
                parsed_para = parse_text(para)
                if parsed_header not in parsed_paras:
                    parsed_paras[parsed_header] = []
                parsed_paras[parsed_header].append(parsed_para)
        return parsed_paras
