import i18n
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from kivy import Logger
from transformers import BertTokenizerFast, EncoderDecoderModel, pipeline
from translate import Translator

import app_config


class TransformerClass:
    def __init__(self, **kwargs):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        Logger.info('Resbailing: Using device: ' + self.device)


class SummarizerClass(TransformerClass):
    def __init__(self, path,max_length=43, **kwargs):
        super().__init__()
        Logger.debug('Resbailing: Initializing summarizer')

        # Summarization parameters
        self.ckpt = app_config.get_current_summarization_model()
        Logger.debug('Resbailing: Loading summarization model')
        if app_config.LANGUAGE == 'es':
            self.tokenizer = BertTokenizerFast.from_pretrained(self.ckpt)
            self.model = EncoderDecoderModel.from_pretrained(self.ckpt).to(self.device)
        elif app_config.LANGUAGE == 'en':
            self.model = pipeline("summarization", model=self.ckpt)

        # Markdown file parameters
        self.pages = None
        self.title = None
        self.path = path
        self.max_length = max_length

    def summarize_text(self, text, max_length=None):
        if max_length is None:
            max_length = self.max_length

        if app_config.LANGUAGE == 'es':
            inputs = self.tokenizer([text], padding="max_length", truncation=True, max_length=max_length, return_tensors="pt")
            input_ids = inputs.input_ids.to(self.device)
            attention_mask = inputs.attention_mask.to(self.device)
            output = self.model.generate(input_ids, attention_mask=attention_mask)
            return self.tokenizer.decode(output[0], skip_special_tokens=True)
        if app_config.LANGUAGE == 'en':
            return self.model(text, max_length=max_length, min_length=5, do_sample=False)[0]['summary_text']


class ImageGeneratorClass(TransformerClass):
    def __init__(self, **kwargs):
        super().__init__()
        Logger.debug('Resbailing: Initializing image generator')
        self.model_id = app_config.IMAGE_GENERATION_MODEL
        # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float32)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.enable_sequential_cpu_offload()
        self.pipe.enable_attention_slicing(2)

        self.image_order = 0

    def generate_image(self, text):
        extra_attrs = "amazing, astonishing, wonderful, beautiful, highly detailed, centered"  # TODO: Make this configurable
        if app_config.LANGUAGE != 'en':
            translator = Translator(to_lang="en", from_lang=app_config.LANGUAGE)
            text = translator.translate(text)
        full_text = f"{text},{extra_attrs}"
        return self.pipe(full_text).images[0]

    def generate_image_to_mdfile(self, text, md_file, session_path):
        try:
            if md_file is None:
                raise ValueError('Markdown file not initialized')
            if session_path is None:
                raise ValueError('Session path not initialized')
        except ValueError:
            Logger.exception('Resbailing:' + ValueError.__str__())

        Logger.debug('Resbailing: Generating image: ' + text[:10] + '...')
        image_path = session_path + "/images/image" + str(self.image_order) + ".png"
        self.image_order += 1
        image_path = image_path.replace(' ', '_')
        image = self.generate_image(text)
        image.save(image_path)
        md_file.new_line("\n![](" + image_path.replace(session_path, '') + ")")
