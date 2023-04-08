# APP ################################################################################################

LANGUAGE = 'en'
DEBUG = True
BASE_PATH = './'
SESSIONS_PATH = BASE_PATH + 'sessions/'

# IMAGE_STORAGE ############################################################################################
IMAGE_STORAGE_SERVICE = 'GoogleDrive'
IMGUR_CLIENT_ID = 'd50cc113493324b'

# SLIDES ##########################################################################################
# If modifying these scopes, delete the file token.json.
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive.file']

# Summarization ####################################################################################
SUMMARIZATION_MODELS = {'es': 'mrm8488/bert2bert_shared-spanish-finetuned-summarization',
                        'en': 'philschmid/flan-t5-base-samsum',}

TITLE_GENERATION_MODELS = {'en': 'deep-learning-analytics/automatic-title-generation'}

SENTENCE_ENCODERS = {'en' : 'https://tfhub.dev/google/universal-sentence-encoder/4'}

if LANGUAGE not in SENTENCE_ENCODERS.keys():
    SENTENCE_ENCODERS[LANGUAGE] = SENTENCE_ENCODERS['en']
SENTENCE_ENCODER = SENTENCE_ENCODERS[LANGUAGE]

# IMAGE GENERATION #################################################################################
IMAGE_GENERATION_MODEL = "stabilityai/stable-diffusion-2-1"


# FUNCTIONS #######################################################################################
def get_current_summarization_model():
    return SUMMARIZATION_MODELS[LANGUAGE]

def get_current_title_generation_model():
    return TITLE_GENERATION_MODELS[LANGUAGE]
