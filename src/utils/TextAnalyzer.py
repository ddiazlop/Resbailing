import numpy
import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as f
from typing import Dict, List

class TextAnalyzerMemorandum:
    def __init__(self, last_sentence: str):
        self.last_sentece = last_sentence

    def reminds_of_last_sentence(self, sentence: str) -> bool:
        return sentence == self.last_sentece

class TextAnalyzer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.memos = []
        self.slides = {}

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

    def compare_sentences(self, sentences : List[str]) -> List[float]:
        sentence_embeddings = self.get_embeddings(sentences)
        similarities = self.get_similarities_with_first_sentence(sentence_embeddings)
        return similarities

    def populate_slides(self, paras : Dict[str, list]) -> None:
        for header, paras in paras.items():
            self.slides[header] = []
            for text in paras:
                sentences = text.split(".")
                sentences = [x.strip() for x in sentences]
                sentences = [x for x in sentences if x != '']

                if len(self.memos) > 0 and len(self.slides[header]) > 0:
                    sentences.insert(0, self.memos[-1].last_sentece)
                    self.slides[header].pop()

                merged_sentences = self.recursive_merge(sentences, [])

                self.memos.append(TextAnalyzerMemorandum(merged_sentences[-1]))
                self.slides[header].extend(merged_sentences)


    def merge_similar_sentences(self, sentences : List[str]) -> (str, int):
        similarities = self.compare_sentences(sentences)
        mean_similarity = self.get_mean_similarity(similarities)
        merged_sentence = ""
        count = 0
        for i in range(len(similarities)):
            if similarities[i ] > mean_similarity:
                merged_sentence += sentences[i] + ". "
                count += 1
        return merged_sentence, count

    def recursive_merge(self, sentences : List[str], merged_sentences : List[str]) -> List[str]:
        if len(sentences) == 0:
            return merged_sentences

        if len(sentences) == 1:
            merged_sentences.append(sentences[0])
            sentences.pop()
            return merged_sentences

        merged_sentence, count = self.merge_similar_sentences(sentences)
        merged_sentences.append(merged_sentence)
        sentences = sentences[count:]

        return self.recursive_merge(sentences, merged_sentences)

