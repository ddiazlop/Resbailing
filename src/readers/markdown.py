import datetime
import io

import panflute
import pypandoc
import torch
from kivy import Logger
from mdutils import MdUtils
from transformers import BertTokenizerFast, EncoderDecoderModel


from src.readers.superclasses.summarizer import SummarizerClass
from src.utils.Docmdutils import count_words, parse_text, new_slide


class MarkdownSummarizer(SummarizerClass):
    def summarize(self):
        Logger.debug('Markdown: Summarizing ' + self.path)
        max_para_words, paras = self.init_content()
        self.summarize_paras(max_para_words, paras)
        self.mdFile.create_md_file()

    def summarize_paras(self, max_para_words, paras):
        Logger.debug('Markdown: Summarizing paragraphs')
        for header in paras.keys():
            if len(paras[header]) > 1:
                for i in range(len(paras[header])):
                    Logger.debug('Markdown: Summarizing paragraph ' + str(i + 1) +'/'+ str(len(paras[header])) +  ' of header ' + parse_text(header))
                    new_slide(self.mdFile, parse_text(header))
                    self.mdFile.new_header(level=2, title=parse_text(header))
                    para = paras[header][i]
                    if count_words(para) < max_para_words[header] / 2:
                        if len(paras[header]) < i + 1:
                            next_para = paras[header][i + 1]
                            if count_words(next_para) != max_para_words[header] / 2:
                                para.content += next_para.content
                                paras[header].remove(next_para)
                                i += 1  # Skip the next paragraph
                    self.mdFile.new_paragraph(self.summarize_text(parse_text(para)))
            else:
                Logger.debug('Markdown: Summarizing paragraph 1/1 of header ' + parse_text(header))
                new_slide(self.mdFile, parse_text(header))
                self.mdFile.new_header(level=2, title=parse_text(header))
                text = parse_text(paras[header][0])
                self.mdFile.new_paragraph(self.summarize_text(text))

    def init_content(self):
        data = pypandoc.convert_file(self.path, 'json')
        doc = panflute.load(io.StringIO(data))
        paras = {}
        max_para_words = {}
        Logger.debug('Markdown: Getting titles and paragraphs')
        for elem in doc.content:
            if isinstance(elem, panflute.Header) and elem.level == 1:
                self.title = parse_text(elem)
                self.mdFile.new_header(level=1, title=self.title)
                last_header = elem
            elif isinstance(elem, panflute.Header):
                last_header = elem
            elif isinstance(elem, panflute.Para):
                paras[last_header] = paras.get(last_header, []) + [elem]
                max_para_words[last_header] = max_para_words.get(last_header, 0) + count_words(elem)
        return max_para_words, paras




