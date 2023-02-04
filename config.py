# APP ################################################################################################
LANGUAGE = 'es'


# SLIDES ##########################################################################################
# If modifying these scopes, delete the file token.json.
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/presentations']


# Summarization ####################################################################################
SUMMARIZATION_MODELS = {'es':'mrm8488/bert2bert_shared-spanish-finetuned-summarization'}





# FUNCTIONS #######################################################################################
def get_current_summarization_model():
    return SUMMARIZATION_MODELS[LANGUAGE]