from __future__ import print_function

import io
import os.path

import panflute
import pypandoc
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from kivy import Logger
from config import GOOGLE_SCOPES as SCOPES

from src.utils.Docmdutils import parse_text




class GoogleSlides:
    def __init__(self, session_path):
        # The session is a markdown file
        self.paras = None
        self.title = None
        self.creds = None
        self.page_id = 0
        self.path = session_path

        self.init_content()
        self.get_credentials()
        self.service = build('slides', 'v1', credentials=self.creds)

    def export(self):
        presentation = self.create_presentation()
        for header, para in self.paras.items():
            self.create_slide(presentation.get('presentationId'), parse_text(header), parse_text(para[0]))
        # Delete the first slide


    def get_credentials(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        token_path = "src/export/token.json"
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        self.creds = creds

    def create_presentation(self):
        try:
            body = {
                'title': self.title
            }
            presentation = self.service.presentations().create(body=body).execute()
            self.set_title_slide(presentation.get('presentationId'))
            Logger.info("Presentation created: " + presentation.get('presentationId'))
            return presentation
        except HttpError as err:
            Logger.error("Presentation creation failed")
            Logger.error("Error code: " + str(err.resp.status))
            Logger.error("Error message: " + err.resp.reason)

    def set_title_slide(self, presentation_id):
        Logger.info("ui/export/google_slides.py: Creating title slide")
        requests = [
            {
                'createSlide': {
                    'objectId': 'pageId' + str(self.page_id),
                    'insertionIndex': str(self.page_id),
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_ONLY'
                    },
                    "placeholderIdMappings": [
                        {
                            "layoutPlaceholder": {
                                "type": "TITLE",
                                "index": 0
                            },
                            "objectId": "titleId" + str(self.page_id)
                        },
                    ]
                }
            },
            {
                'insertText': {
                    'objectId': 'titleId' + str(self.page_id),
                    'text': self.title
                },
            },
        ]
        self.send_batch_update(presentation_id, requests)
        self.page_id += 1

    def create_slide(self, presentation_id, title, body):
        try:
            requests = [
                {
                    'createSlide': {
                        'objectId': 'pageId' + str(self.page_id),
                        'insertionIndex': str(self.page_id),
                        'slideLayoutReference': {
                            'predefinedLayout': 'TITLE_AND_BODY'
                        },
                        "placeholderIdMappings": [
                            {
                                "layoutPlaceholder": {
                                    "type": "TITLE",
                                    "index": 0
                                },
                                "objectId": "titleId" + str(self.page_id)
                            },
                            {
                                "layoutPlaceholder": {
                                    "type": "BODY",
                                    "index": 0
                                },
                                "objectId": "bodyId" + str(self.page_id)
                            }
                        ]
                    }
                },
                {
                    'insertText': {
                        'objectId': 'titleId' + str(self.page_id),
                        'text': title
                    },
                },
                {
                    'insertText': {
                        'objectId': 'bodyId' + str(self.page_id),
                        'text': body
                    },
                }
            ]
            self.send_batch_update(presentation_id, requests)
            Logger.info("Created slide with ID: " + 'pageId' + str(self.page_id))
            self.page_id += 1
        except HttpError as err:
            Logger.error("Slide creation failed")
            Logger.error("Error code: " + str(err.resp.status))
            Logger.error("Error message: " + err.resp.reason)


    def send_batch_update(self, presentation_id, requests):
        try:
            body = {
                'requests': requests
            }

            response = self.service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
            Logger.debug("Batch update response: " + str(response))
            return response

        except HttpError as err:
            Logger.error("src/export/google_slides.py: Batch update failed")
            Logger.error("Error code: " + str(err.resp.status))
            Logger.error("Error message: " + err.resp.reason)

    def init_content(self):
        data = pypandoc.convert_file(self.path, 'json')
        doc = panflute.load(io.StringIO(data))
        paras = {}
        Logger.debug('Markdown: Getting titles and paragraphs')
        for elem in doc.content:
            if isinstance(elem, panflute.Header) and elem.level == 1:
                self.title = parse_text(elem)
                last_header = elem
            elif isinstance(elem, panflute.Header):
                last_header = elem
            elif isinstance(elem, panflute.Para):
                paras[last_header] = paras.get(last_header, []) + [elem]
        self.paras = paras