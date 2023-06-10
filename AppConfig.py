import yaml

from src.i18n import Translator


class AppConfig:
    yaml_file = 'config.yaml'
    config = None

    def __init__(self):
        self.load_config()

    def load_config(self):
        with open(self.yaml_file, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def save_config(self):
        Translator.change_language(self.language)
        with open(self.yaml_file, 'w') as f:
            yaml.dump(self.config, f)

    @property
    def language(self) -> str:
        return self.config['LANGUAGE']

    @language.setter
    def language(self, value:str):
        self.config['LANGUAGE'] = value

    @property
    def languages(self) -> list:
        return self.config['LANGUAGES']

    @property
    def debug(self) -> bool:
        return self.config['DEBUG']

    @property
    def base_path(self) -> str:
        return self.config['BASE_PATH']

    @property
    def sessions_path(self) -> str:
        return self.base_path + 'sessions/'

    @property
    def image_storage_service(self) -> str:
        return self.config['IMAGE_STORAGE_SERVICE']

    @property
    def google_scopes(self) -> list:
        return self.config['GOOGLE_SCOPES']

    @property
    def title_generation_models(self) -> dict:
        return self.config['TITLE_GENERATION_MODELS']

    @property
    def sentence_encoders(self) -> dict:
        return self.config['SENTENCE_ENCODERS']

    @property
    def sentence_encoder(self) -> str:
        return self.sentence_encoders[self.language] if self.language in self.sentence_encoders.keys() else self.sentence_encoders['en']

    @property
    def image_generation_model(self) -> dict:
        return self.config['IMAGE_GENERATION_MODEL']

    @property
    def summarization_model(self) -> str:
        return self.config['SUMMARIZATION_MODEL']

    @property
    def title_generation_model(self) -> str:
        return self.config['TITLE_GENERATION_MODEL']

app_config = AppConfig()