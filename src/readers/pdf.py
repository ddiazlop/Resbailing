import datetime

import pdfplumber
from kivy import Logger
from mdutils import MdUtils
# from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
# import torch

import torch
from transformers import BertTokenizerFast, EncoderDecoderModel


class PdfAnalyzer:
    def __init__(self, path):
        Logger.debug('src/pdf.py: Initializing PDF analyzer')
        # Summarization parameters
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.ckpt = 'mrm8488/bert2bert_shared-spanish-finetuned-summarization'
        self.tokenizer = BertTokenizerFast.from_pretrained(self.ckpt)
        Logger.debug('src/pdf.py: Loading summarization model')
        self.model = EncoderDecoderModel.from_pretrained(self.ckpt).to(self.device)

        # Markdown file parameters
        self.subtitle = None
        self.pages = None
        self.title = None
        today = datetime.date.today()
        hour = datetime.datetime.now().strftime("%H")
        self.mdFile = MdUtils(file_name="sessions/" + today.__str__() + "_" + hour, title=today.__str__())
        self.path = path

    def full_analysis(self):
        self.action(['first_slide', 'presentation'])

    def action(self, actions, *args):
        Logger.debug('PDF: Reading PDF' + self.path + " ##### Actions: " + str(actions))
        actions = {
            'first_slide': self.generate_first_slide,
            'presentation': self.generate_presentation
        }

        with pdfplumber.open(self.path) as pdf:
            self.pages = pdf.pages
            for action in actions:
                actions[action]()

        self.mdFile.create_md_file()
        
        
    def generate_first_slide(self):
        Logger.debug('PDF: Generating first slide')
        self.mdFile.new_line('---')
        first_page = self.pages[0]
        word_dict = self.get_word_sizes_dict(first_page)

        title, words_same_height, highest_word = self.get_title(word_dict)
        self.mdFile.new_header(level=1, title=title)
        self.title = title

        self.subtitle = self.get_subtitle(word_dict, words_same_height, highest_word)
        self.mdFile.new_header(level=2, title=self.subtitle)

        # self.generate_image(title)

        pass

    def generate_presentation(self):
        Logger.debug('PDF: Generating presentation')
        self.mdFile.new_line('---')
        # Delete both the title and subtitle then check if there are any words left
        # If there are, then generate a new slide
        first_page = self.pages[0]
        words = first_page.extract_words()
        word_list = [word for word in words if word['text'] not in self.title and word['text'] not in self.subtitle]

        # TODO: Variation for documents with data on the first page
        # if len(word_list) > 10:
        #     self.generate_slide(first_page)

        for page in self.pages[1:]:
            self.generate_slide(page)

        pass


    def generate_slide(self, page):
        Logger.debug('PDF: Generating slide from page ' + str(page.page_number))
        self.mdFile.new_line('---')
        text = page.extract_text()
        summary = self.generate_summary(text)

        i = 0

    def generate_summary(self, text):
        inputs = self.tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        input_ids = inputs.input_ids.to(self.device)
        attention_mask = inputs.attention_mask.to(self.device)
        output = self.model.generate(input_ids, attention_mask=attention_mask)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    @staticmethod
    def get_subtitle(word_dict, words_same_height, highest_word):
        if len(words_same_height) < len(word_dict):
            # Check for subtitle.
            # Get the word with the second highest height
            second_highest_word = max(word_dict, key=lambda key: word_dict[key]['height'] and word_dict[key]['height'] <
                                                                 word_dict[highest_word]['height'])
            subtitle_words = [word for word in word_dict if
                              word_dict[word]['height'] == word_dict[second_highest_word]['height']]
            subtitle = ' '.join(subtitle_words)
        return subtitle

    @staticmethod
    def get_title(word_dict):
        # Get the word with the highest height
        highest_word = max(word_dict, key=lambda key: word_dict[key]['height'])
        # Extract the title given the highest word
        words_same_height = [word for word in word_dict if
                             word_dict[word]['height'] == word_dict[highest_word]['height']]
        words_same_height.sort(
            key=lambda key: word_dict[key]['word_count'] and word_dict[key]['top'] - word_dict[highest_word][
                'top'] < 10)
        title = ' '.join(words_same_height)
        return title, words_same_height, highest_word

    @staticmethod
    def get_word_sizes_dict(first_page):
        first_page_words = first_page.extract_words()
        word_dict = {}
        word_count = 0
        for word in first_page_words:
            height = word['bottom'] - word['top']
            if word['text'] in word_dict:
                # Compare the size of the word with the size of the previous word
                if height > word_dict[word['text']]['height']:
                    word_dict[word['text']] = {'height': height, 'top': word['top'], 'word_count': word_count}
            else:
                # Save the height used for that word and its position relative to the top of the page
                # Also save the word count
                word_dict[word['text']] = {'height': height, 'top': word['top'], 'word_count': word_count}
        return word_dict

    ############# PREGUNTAR ################
    # @staticmethod
    # def generate_image(prompt):
    #     pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    #     pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    #     pipe = pipe.to("cuda")
    #
    #     image = pipe(prompt).images[0]
    #     image_name = prompt.replace(" ", "_") + ".png"
    #     image.save("sessions/images/" + image_name)
