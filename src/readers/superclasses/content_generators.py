import datetime

import torch
from kivy import Logger
from mdutils import MdUtils
from transformers import BertTokenizerFast, EncoderDecoderModel
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
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
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe = self.pipe.to(self.device)

    def generate_image(self, text):
        return self.pipe(text).images[0]

    def generate_image_to_mdfile(self, text):
        try:
            if self.mdFile is None:
                raise ValueError('Markdown file not initialized')
            if self.session_path is None:
                raise ValueError('Session path not initialized')
        except ValueError:
            Logger.exception('src/superclasses/image_generator.py:' + ValueError.__str__())

        Logger.debug('src/superclasses/image_generator.py: Generating image: ' + text[:10] + '...')
        image = self.generate_image(text)
        image.save(self.session_path + "/images/" + text[:10] + ".png")
        self.mdFile.new_line("![](" + self.session_path + "/images/" + text[:10] + ".png)")



