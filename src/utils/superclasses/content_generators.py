import datetime
import os

import torch
from kivy import Logger
from mdutils import MdUtils
from transformers import BertTokenizerFast, EncoderDecoderModel
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from translate import Translator

import app_config


class TransformerClass:
    def __init__(self, **kwargs):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        Logger.info('src/superclasses/content_generators.py: Using device: ' + self.device)


class SummarizerClass(TransformerClass):
    def __init__(self, path, **kwargs):
        super().__init__()
        Logger.debug('src/superclasses/content_generators.py: Initializing summarizer')

        # Summarization parameters
        self.ckpt = app_config.get_current_summarization_model()
        self.tokenizer = BertTokenizerFast.from_pretrained(self.ckpt)
        Logger.debug('src/markdown.py: Loading summarization model')
        self.model = EncoderDecoderModel.from_pretrained(self.ckpt).to(self.device)

        # Markdown file parameters
        self.pages = None
        self.title = None
        self.path = path

    def summarize_text(self, text):
        inputs = self.tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        input_ids = inputs.input_ids.to(self.device)
        attention_mask = inputs.attention_mask.to(self.device)
        output = self.model.generate(input_ids, attention_mask=attention_mask)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)


class ImageGeneratorClass(TransformerClass):
    def __init__(self, **kwargs):
        super().__init__()
        Logger.debug('src/superclasses/image_generator.py: Initializing image generator')
        self.model_id = app_config.IMAGE_GENERATION_MODEL
        # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float32)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        # self.pipe = self.pipe.to(self.device)
        self.pipe.enable_sequential_cpu_offload()
        self.pipe.enable_attention_slicing(2)

    def generate_image(self, text):
        extra_attrs = "photo, photography –s 625 –q 2 –iw 3" #TODO: Make this configurable
        translator = Translator(to_lang="en", from_lang=app_config.LANGUAGE) #TODO: Case sensitive if default is english
        translation = translator.translate(text)
        full_text = f"{text},{extra_attrs}"
        return self.pipe(full_text).images[0]

    def generate_image_to_mdfile(self, text):
        try:
            if self.mdFile is None:
                raise ValueError('Markdown file not initialized')
            if self.session_path is None:
                raise ValueError('Session path not initialized')
        except ValueError:
            Logger.exception('src/superclasses/image_generator.py:' + ValueError.__str__())

        Logger.debug('src/superclasses/image_generator.py: Generating image: ' + text[:10] + '...')
        image_path = self.session_path + "/images/" + text[:10]+ ".png"
        image_path = image_path.replace(' ', '_')
        image = self.generate_image(text)
        image.save(image_path)
        self.mdFile.new_line("\n![](" + image_path.replace(self.session_path, '') + ")")



