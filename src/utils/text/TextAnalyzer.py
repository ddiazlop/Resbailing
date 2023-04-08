import re
from enum import Enum

import numpy
import torch
from kivy import Logger
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as f
from typing import Dict, List

class LastSentenceMemorandum:
    def __init__(self, last_sentence: str):
        self.last_sentece = last_sentence

    def reminds_of_last_sentence(self, sentence: str) -> bool:
        return sentence == self.last_sentece

class ThresholdMemorandum:
    def __init__(self, threshold: float):
        self.threshold = threshold

class ThresholdMode(Enum):
    MEAN = 1
    MEDIAN = 2
    FIXED_MEAN = 3
    FIXED_MEDIAN = 4

class TextAnalyzer:
    def __init__(self, threshold_mode: ThresholdMode = ThresholdMode.FIXED_MEAN):
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.memos = []
        self.threshold_memos = []
        self.slides = {}
        self.threshold_mode = threshold_mode

    def encode_input(self, sentences : list):
        return self.tokenizer(sentences, padding=True, truncation=True, max_length=512, return_tensors='pt')

    def get_output(self, encoded_input):
        with torch.no_grad():
            model_output = self.model(**encoded_input)

        return model_output

    @staticmethod
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_embeddings(self, sentences : list):
        encoded_input = self.encode_input(sentences)
        model_output = self.get_output(encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = f.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings

    @staticmethod
    def get_similarities_with_first_sentence(sentence_embeddings):
        return  [x for x in numpy.inner(sentence_embeddings[0], sentence_embeddings)]

    @staticmethod
    def get_mean_similarity(similarities):
        return numpy.mean(similarities)

    def get_fixed_mean_similarity(self, similarities):
        if len(self.threshold_memos)<=0:
            self.threshold_memos.append(ThresholdMemorandum(float(numpy.mean(similarities))))
            return self.threshold_memos[0].threshold
        return self.threshold_memos[0].threshold


    @staticmethod
    def get_median_similarity(similarities):
        return numpy.median(similarities)

    def get_fixed_median_similarity(self, similarities):
        if len(self.threshold_memos)<=0:
            self.threshold_memos.append(ThresholdMemorandum(float(numpy.median(similarities))))
            return self.threshold_memos[0].threshold
        return self.threshold_memos[0].threshold

    def compare_sentences(self, sentences : List[str]) -> List[float]:
        """Compare the given sentences to the first sentence in the list and return a list of similarities."""
        sentence_embeddings = self.get_embeddings(sentences)
        similarities = self.get_similarities_with_first_sentence(sentence_embeddings)
        return similarities

    def populate_slides(self, paras : Dict[str, list]) -> None:
        """Populate the slides dictionary with the given paragraphs

        **Args:** Takes a dictionary with headers as keys and a list of paragraphs as values. That usually looks like this:
            {
                "Header 1": ["Paragraph 1", "Paragraph 2"],
                "Header 2": ["Paragraph 3", "Paragraph 4"]
            }
        """
        for header, paras in paras.items():
            self.slides[header] = []
            full_text = " ".join(paras)
            sentences = self.split_into_sentences(full_text)
            merged_sentences = self.recursive_merge(sentences, [])
            self.slides[header].extend(merged_sentences)


    def merge_similar_sentences(self, sentences : List[str], mode : ThresholdMode) -> (str, int):
        merged_sentence = sentences[0]
        sentences_aux = sentences[1:].copy()
        count = 1
        num_sentences = len(sentences_aux)
        for i in range(num_sentences):
            sentences_aux.insert(0, merged_sentence)
            similarities = self.compare_sentences(sentences_aux)
            sim_threshold = self.get_sim_threshold(mode, similarities[1:])
            Logger.debug("Resbailing: Similarities: " + str(sim_threshold))
            if similarities[i+1] > sim_threshold:
                merged_sentence += ". " + sentences_aux[i + 1]
                count += 1
            else:
                break
            sentences_aux.pop(0)
        return merged_sentence, count

    def get_sim_threshold(self, mode, similarities):
        if mode == ThresholdMode.MEAN:
            sim_threshold = self.get_mean_similarity(similarities)
        elif mode == ThresholdMode.MEDIAN:
            sim_threshold = self.get_median_similarity(similarities)
        elif mode == ThresholdMode.FIXED_MEAN:
            sim_threshold = self.get_fixed_mean_similarity(similarities)
        elif mode == ThresholdMode.FIXED_MEDIAN:
            sim_threshold = self.get_fixed_median_similarity(similarities)
        else:
            Logger.error("Resbailing: Threshold mode not implemented")
            raise NotImplementedError("Threshold mode not implemented")
        return sim_threshold

    def recursive_merge(self, sentences : List[str], merged_sentences : List[str]) -> List[str]:
        """Recursively merge similar sentences, comparing the first sentence with the rest of the sentences in each iteration"""
        if len(sentences) == 0:
            return merged_sentences

        if len(sentences) == 1:
            merged_sentences.append(sentences[0])
            return merged_sentences

        merged_sentence, count = self.merge_similar_sentences(sentences, self.threshold_mode)
        merged_sentences.append(merged_sentence)
        sentences = sentences[count:]

        return self.recursive_merge(sentences, merged_sentences)

    @staticmethod
    def split_into_sentences(text : str) -> List[str]:
        """Split text into sentences using the period as a delimiter"""
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
        sentences = [x.strip() for x in sentences]
        sentences = [x for x in sentences if x != '']
        return sentences

