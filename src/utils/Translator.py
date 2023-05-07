from typing import List

from translate import Translator as Trans

def trans_to_en(text):
    translation = Trans(provider='mymemory', to_lang='en', from_lang='es', email='akeforne@gmail.com').translate(text)
    return translation

def trans_to_es(text):
    translation = Trans(provider='mymemory', to_lang='es', from_lang='en', email='akeforne@gmail.com').translate(text)
    return translation

def cut_text(text : str, max_length: int) -> List[str]:
    """
    Cuts a text into multiple texts of max_length characters
    :param text:
    :param max_length:
    :return:
    """
    if len(text) > max_length:
        words = text.split()
        curr_text = ''
        output = []
        for word in words:
            if len(curr_text + word) + 1 <= max_length:
                curr_text += word + ' '
            else:
                output.append(curr_text.strip())
                curr_text = word + ' '
        output.append(curr_text.strip())
        return output

def trans_large_to_en(text : str) -> str:
    text_parts = cut_text(text, 500)
    output = ''
    if text_parts is None:
        return trans_to_en(text)
    for part in text_parts:
        translated = trans_to_en(part)
        output += translated + ' '
    return output