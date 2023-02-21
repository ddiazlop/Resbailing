# APP ################################################################################################
import os

LANGUAGE = 'es'
DEBUG = False
BASE_PATH = './'
SESSIONS_PATH = BASE_PATH + 'sessions/'

# IMAGE_STORAGE ############################################################################################
IMAGE_STORAGE_SERVICE = 'GoogleDrive'
IMGUR_CLIENT_ID = 'd50cc113493324b'

# SLIDES ##########################################################################################
# If modifying these scopes, delete the file token.json.
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive.file']


# Summarization ####################################################################################
SUMMARIZATION_MODELS = {'es':'mrm8488/bert2bert_shared-spanish-finetuned-summarization', 'en':'facebook/bart-large-cnn'}


# IMAGE GENERATION #################################################################################
IMAGE_GENERATION_MODEL = "stabilityai/stable-diffusion-2-1"

# FUNCTIONS #######################################################################################
def get_current_summarization_model():
    return SUMMARIZATION_MODELS[LANGUAGE]