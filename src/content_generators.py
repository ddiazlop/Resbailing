import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from kivy import Logger
from mdutils import MdUtils
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

from src.utils.Translator import trans_large_to_en
from AppConfig import app_config


class TransformerClass:
    def __init__(self, **kwargs):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        Logger.info('Resbailing: Using device: ' + self.device)
        if self.device not in ['cuda']:
            raise ValueError('Resbailing: Device not supported')


class SummarizerClass(TransformerClass):
    def __init__(self, path,max_length=43):
        super().__init__()
        Logger.debug('Resbailing: Initializing summarizer')

        # Summarization parameters
        ckpt = app_config.summarization_model
        title_ckpt = app_config.title_generation_model
        Logger.debug('Resbailing: Loading summarization model')

        self.model = pipeline("summarization", model=ckpt)
        self.title_tokenizer = AutoTokenizer.from_pretrained(title_ckpt)
        self.title_model = AutoModelForSeq2SeqLM.from_pretrained(title_ckpt)

        # Markdown file parameters
        self.pages = None
        self.title = None
        self.path = path
        self.max_length = max_length



    def generate_title(self, text):
        if app_config.language == 'es':
            text = trans_large_to_en(text)

        inputs = self.title_tokenizer(text, padding="max_length", truncation=True, max_length=100, return_tensors="pt")
        inputs = {'input_ids': inputs['input_ids'], 'attention_mask': inputs['attention_mask']}
        outputs = self.title_model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], do_sample=True,
                                                max_length=120,
                                                top_p=0.95,
                                                top_k=60,
                                                early_stopping=True,
                                                num_return_sequences=1)
        answer = self.title_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer

    def summarize_text(self, text, max_length=None):
        if app_config.language == 'es':
            text = trans_large_to_en(text)

        if max_length is None:
            max_length = self.max_length


        summary = self.model(text, max_length=max_length, min_length=5)
        return summary[0]['summary_text']


class ImageGeneratorClass(TransformerClass):
    def __init__(self):
        super().__init__()
        Logger.debug('Resbailing: Initializing image generator')
        self.model_id = app_config.image_generation_model
        # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float32)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.enable_sequential_cpu_offload()
        self.pipe.enable_attention_slicing()



    def generate_image(self, text):
        extra_attrs = "amazing, astonishing, wonderful, beautiful, highly detailed, centered, trending on artstation"
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



    def generate_background_image(self, text, session_path, default = True):
        if not default:
            extra_attrs = "cool geometric white background, minimalistic shapes, professional slideshow, wallpaper"
            full_text = f"{extra_attrs},{text}"
            background = self.pipe(full_text).images[0]
            background_path = session_path + "/images/background.png"
            background.save(background_path)
        else:
            with open(app_config.base_path + '/src/export/media/background.png', 'rb') as f:
                background = f.read()
            background_path = session_path + "/images/background.png"

            with open(background_path, 'wb') as f:
                f.write(background)


    @staticmethod
    def place_image_to_mdfile(image_path:str, session_path:str, md_file : MdUtils):
        image_path = '/images/' + image_path
        md_file.new_line("\n![](" + image_path.replace(session_path, '') + ")")
