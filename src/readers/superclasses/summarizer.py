import datetime

import torch
from kivy import Logger
from mdutils import MdUtils
from transformers import BertTokenizerFast, EncoderDecoderModel
import config





class SummarizerClass:
    def __init__(self, path):
        Logger.debug('src/superclasses/summarizer.py: Initializing summarizer')
        # Summarization parameters
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.ckpt = config.get_current_summarization_model()
        self.tokenizer = BertTokenizerFast.from_pretrained(self.ckpt)
        Logger.debug('src/markdown.py: Loading summarization model')
        self.model = EncoderDecoderModel.from_pretrained(self.ckpt).to(self.device)

        # Markdown file parameters
        self.pages = None
        self.title = None
        today = datetime.date.today()
        hour = datetime.datetime.now().strftime("%H")
        self.mdFile = MdUtils(file_name="sessions/" + today.__str__() + "_" + hour, title=today.__str__())
        self.path = path

    def summarize_text(self, text):
        inputs = self.tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        input_ids = inputs.input_ids.to(self.device)
        attention_mask = inputs.attention_mask.to(self.device)
        output = self.model.generate(input_ids, attention_mask=attention_mask)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

