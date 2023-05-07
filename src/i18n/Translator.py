import re

import yaml
from typing import Dict

lang = 'en'
lang_dir = ''


def init_translator(language:str, languages_dir:str) -> None:
    global lang
    global lang_dir
    lang = language
    lang_dir = languages_dir

def change_language(language:str) -> None:
    global lang
    lang = language

def t(code : str) -> str:
    """
    Translate a text code to the current language
    :param code: String formatted as "subfolder.text_code"
    :return:
    """

    try:
        regex = r'^\w+\.\w+$'  # Regex to check if the code is valid
        if not re.match(regex, code):
            raise ValueError("Invalid code format. Expected format: '{subfolder}.text_code'")
    except ValueError as e:
        return str(e)

    code = code.split('.')
    subfolder = code[0]
    text_code = code[1]

    dictt = load_dict(subfolder)

    try:
        return dictt[text_code]
    except KeyError:
        raise KeyError("Text code '{}' not found in '{}'".format(text_code, subfolder))


def load_dict(subfolder : str) -> Dict[str, str]:
    """
    Loads a dictionary from a yml file
    :param subfolder:
    :return:
    """
    # Load the file
    try:
        with open(r'{}/{}/{}.yml'.format(lang_dir, subfolder, lang), 'r', encoding='utf8') as file:
            dictt = yaml.load(file, Loader=yaml.FullLoader)
            return dictt
    except FileNotFoundError:
        with open(r'./ui/i18n/{}/{}.yml'.format(subfolder, lang), 'r', encoding='utf8') as file:
            dictt = yaml.load(file, Loader=yaml.FullLoader)
            return dictt
