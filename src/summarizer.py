import datetime
import io
import os

import i18n
import numpy
import panflute
import pypandoc
import torch
from kivy import Logger
from mdutils import MdUtils
from transformers import AutoTokenizer, AutoModel

import app_config
import torch.nn.functional as F
from src.utils.Docmdutils import count_words, parse_text
from src.content_generators import SummarizerClass, ImageGeneratorClass


class MarkdownSummarizer(SummarizerClass, ImageGeneratorClass):
    def __init__(self, path, loading_screen):
        self.update_loading_info = loading_screen.update_info
        today = datetime.date.today()
        # Create a folder for the session and its images
        session = "sessions/" + today.__str__()
        if not os.path.exists(session):
            os.mkdir(session)
            os.mkdir(session + "/images")
        self.session_path = session
        self.mdFile = MdUtils(file_name=self.session_path + "/presentation", title=today.__str__())
        super().__init__(path=path)

        self.update_loading_info(i18n.t('dict.loading_summarization_model'))

    def summarize(self):
        Logger.debug('src/readers/summarizer.py: Summarizing ' + self.path)
        self.update_loading_info(i18n.t('dict.summarizing'))
        max_para_words, paras = self.init_content()
        self.get_paras_corr(paras)
        # self.summarize_paras_lazy(paras)
        self.mdFile.create_md_file()

    @staticmethod
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_paras_corr(self, paras):
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.update_loading_info(i18n.t('dict.encoding_text'))
        slides = {}
        for header in paras:
            parsed_header = parse_text(header)
            slides[parsed_header] = []
            previus_text = ''
            for para in paras[header]:
                text = parse_text(para)
                sentences = text.split(".")
                sentences = [x.strip() for x in sentences]
                sentences.insert(0, previus_text) # This way we force checking the similarity with the previous paragraph
                sentences = [x for x in sentences if x != '']
                sentences_aux = sentences.copy()

                for sentence in sentences:
                    if len(sentences_aux) > 1 and sentence in sentences_aux:
                        if parsed_header == "Conclusion":
                            i = 0
                        encoded_input = tokenizer(sentences_aux, padding=True, truncation=True, max_length=512, return_tensors='pt')
                        with torch.no_grad():
                            model_output = model(**encoded_input)

                        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
                        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

                        similarities_with_first_sentence = [x for x in numpy.inner(sentence_embeddings[0], sentence_embeddings[1:])]
                        # similarities_mean = numpy.mean(similarities_with_first_sentence)
                        similarities_mean = 0.3

                        text_to_resume = sentence

                        # Prevent repeating the same paragraph
                        if text_to_resume is previus_text:
                            slides[parsed_header].__delitem__(-1)


                        sentences_aux.__delitem__(0)
                        for i, x in enumerate(similarities_with_first_sentence):
                            if x >= similarities_mean:
                                text_to_resume += " " + sentences_aux[0]
                                sentences_aux.__delitem__(0)
                            else:
                                break

                        previus_text = text_to_resume
                        slides[parsed_header].append(text_to_resume)
                    elif sentence not in previus_text and sentence in sentences_aux:
                        slides[parsed_header].append(sentence)

                previus_text = slides[parsed_header][-1]


        for header, paras in slides.items():
            for para in paras:
                self.update_loading_info(i18n.t('dict.summarizing_paragraph') + ' ' + str(paras.index(para) + 1) + '/' + str(
                    len(paras)) + ' ' + i18n.t('dict.of_header') + ' ' + header)
                self.new_slide_parsed(header, para)


    def summarize_paras_lazy(self, paras):
        Logger.debug('src/readers/summarizer.py: Summarizing paragraphs')
        for header in paras.keys():
            num_paras = len(paras[header])
            if num_paras > 1:
                for i in range(len(paras[header])):
                    if i >= len(paras[header]):
                        break
                    if i < len(paras[header]):
                        para = paras[header][i]
                        # Extend the paragraph to make it longer
                        j = self.extend_para(header, i, num_paras, para, paras)

                    Logger.debug('src/readers/summarizer.py: Summarizing paragraph ' + str(i + 1) + '->' + str(i+1+j) + '/' + str(
                            len(paras[header])) + ' of header ' + parse_text(header))
                    self.update_loading_info(i18n.t('dict.summarizing_paragraph') + ' ' + str(i + 1) + '->' + str(i+1+j) + '/' + str(
                            len(paras[header])) + ' ' + i18n.t('dict.of_header') + ' ' + parse_text(header))
                    self.new_slide(header, para)

            else:
                Logger.debug('src/readers/summarizer.py: Summarizing paragraph 1/1 of header ' + parse_text(header))

                self.new_slide(header, paras[header][0])

    @staticmethod
    def extend_para(header, i, num_paras, para, paras):
        j = 0
        for j in range(int(num_paras / 5)):
            if len(paras[header]) > i + 1:
                next_para = paras[header][i + 1]
                para.content += next_para.content
                paras[header].remove(next_para)
        return j


    def new_slide(self, header, para):
        self.slide_break()
        self.mdFile.new_header(level=2, title=parse_text(header))
        summarized_text = self.summarize_text(parse_text(para))
        self.mdFile.new_paragraph(summarized_text)
        self.generate_image_to_mdfile(summarized_text)

    def new_slide_parsed(self, header, para):
        self.slide_break()
        self.mdFile.new_header(level=2, title=header)
        summarized_text = self.summarize_text(para)
        self.mdFile.new_paragraph(summarized_text)
        self.generate_image_to_mdfile(summarized_text)

    def slide_break(self):
        self.mdFile.new_line('\n---\n')

    def init_content(self):
        data = pypandoc.convert_file(self.path, 'json')
        doc = panflute.load(io.StringIO(data))
        paras = {}
        max_para_words = {}
        Logger.debug('src/readers/summarizer.py: Getting titles and paragraphs')
        self.update_loading_info(i18n.t('dict.getting_titles_and_paragraphs'))
        for elem in doc.content:
            if isinstance(elem, panflute.Header) and elem.level == 1:
                self.title = parse_text(elem)
                self.mdFile.new_header(level=1, title=self.title)
                last_header = elem
            elif isinstance(elem, panflute.Header):
                last_header = elem
            elif isinstance(elem, panflute.Para):
                paras[last_header] = paras.get(last_header, []) + [elem]
                num_words = count_words(elem)
                if num_words > max_para_words.get(last_header, 0):
                    max_para_words[last_header] = num_words
        return max_para_words, paras
