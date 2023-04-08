import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from kivy import Logger
from mdutils import MdUtils
from transformers import BertTokenizerFast, EncoderDecoderModel, pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from translate import Translator

import app_config


class TransformerClass:
    def __init__(self, **kwargs):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        Logger.info('Resbailing: Using device: ' + self.device)


class SummarizerClass(TransformerClass):
    def __init__(self, path,max_length=43):
        super().__init__()
        Logger.debug('Resbailing: Initializing summarizer')

        # Summarization parameters
        ckpt = app_config.get_current_summarization_model()
        title_ckpt = app_config.get_current_title_generation_model()
        Logger.debug('Resbailing: Loading summarization model')
        if app_config.LANGUAGE == 'es':
            self.tokenizer = BertTokenizerFast.from_pretrained(ckpt)
            self.model = EncoderDecoderModel.from_pretrained(ckpt).to(self.device)
        elif app_config.LANGUAGE == 'en':
            self.model = pipeline("summarization", model=ckpt)

            self.title_tokenizer = AutoTokenizer.from_pretrained(title_ckpt)
            self.title_model = AutoModelForSeq2SeqLM.from_pretrained(title_ckpt)

        # Markdown file parameters
        self.pages = None
        self.title = None
        self.path = path
        self.max_length = max_length


    def generate_title(self, text):
        if app_config.LANGUAGE == 'en':
            inputs = self.title_tokenizer(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
            inputs = {'input_ids': inputs['input_ids'], 'attention_mask': inputs['attention_mask']}
            outputs = self.title_model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], do_sample=True,
                                                max_length=120,
                                                top_p=0.95,
                                                top_k=60,
                                                early_stopping=True,
                                                num_return_sequences=1)
            answer = self.title_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return answer
        else:
            return text

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
            summary = self.model(text, max_length=max_length, min_length=5)
            return summary[0]['summary_text']


class ImageGeneratorClass(TransformerClass):
    def __init__(self):
        super().__init__()
        Logger.debug('Resbailing: Initializing image generator')
        self.model_id = app_config.IMAGE_GENERATION_MODEL
        # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float32)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.enable_sequential_cpu_offload()
        self.pipe.enable_attention_slicing(2)


    def generate_image(self, text):
        extra_attrs = "amazing, astonishing, wonderful, beautiful, highly detailed, centered, trending on artstation"  # TODO: Make this configurable
        if app_config.LANGUAGE != 'en':
            translator = Translator(to_lang="en", from_lang=app_config.LANGUAGE)
            text = translator.translate(text)
        full_text = f"{text},{extra_attrs}"
        return self.pipe(full_text).images[0]

    def generate_image_to_mdfile(self, text, md_file, session_path, slide_count):
        try:
            if md_file is None:
                raise ValueError('Markdown file not initialized')
            if session_path is None:
                raise ValueError('Session path not initialized')
        except ValueError:
            Logger.exception('Resbailing:' + ValueError.args[0])

        Logger.debug('Resbailing: Generating image: ' + text[:10] + '...')
        image_path = session_path + "/images/image" + str(slide_count) + ".png"
        image = self.generate_image(text)
        image.save(image_path)
        md_file.new_line("\n![](" + image_path.replace(session_path, '') + ")")


    @staticmethod
    def place_image_to_mdfile(image_path:str, session_path:str, md_file : MdUtils):
        image_path = '/images/' + image_path
        md_file.new_line("\n![](" + image_path.replace(session_path, '') + ")")
