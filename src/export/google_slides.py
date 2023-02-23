from __future__ import print_function

import io
import os.path

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from imgurpython import ImgurClient

import panflute
import pypandoc
from PIL import Image
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from kivy import Logger

import requests as req

import app_config
from app_config import GOOGLE_SCOPES as SCOPES

from src.utils.Docmdutils import parse_text




class GoogleSlides:
    def __init__(self, session_manager):
        # The session is a markdown file
        self.folder_id = None
        self.images = None
        self.paras = None
        self.title = None
        self.creds = None
        self.page_id = 0
        self.path = session_manager.current_session_md
        self.current_session = session_manager.current_session_name
        self.imgur_client = ImgurClient(app_config.IMGUR_CLIENT_ID, None)

        self.init_content()
        self.get_credentials()
        self.service = build('slides', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def export(self):
        presentation = self.create_presentation()
        self.create_folder_in_drive("Resbailing")
        for header, para in self.paras.items():
            self.create_slide(presentation.get('presentationId'), parse_text(header), parse_text(para[0]))
        if len(self.images) > 0:
            self.insert_images(presentation.get('presentationId'))
        self.move_files_to_folder(presentation.get('presentationId'))


    def create_folder_in_drive(self, folder_name):
        try:
            # Find if folder already exists
            page_token = None
            while True:
                response = self.drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                           spaces='drive',
                                                           fields='nextPageToken, files(id, name)',
                                                           pageToken=page_token).execute()
                for file in response.get('files', []):
                    if file.get('name') == folder_name:
                        self.folder_id = file.get('id') #TODO: If folder gets deleted, this still points to the old folder
                        return
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = self.drive_service.files().create(body=file_metadata,
                                               fields='id').execute()
            self.folder_id = file.get('id')
        except HttpError as e:
            Logger.error('FolderCreationError: {}'.format(e))

    def move_files_to_folder(self, file_id):
        try:
            file = self.drive_service.files().get(fileId=file_id,
                                                  fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            file = self.drive_service.files().update(fileId=file_id,
                                                     addParents=self.folder_id,
                                                     removeParents=previous_parents,
                                                     fields='id, parents').execute()
            Logger.info('FileMoveToFolderSuccess: Moved file with id' + file.get('id') + ' to folder with id' + self.folder_id)
        except HttpError as e:
            Logger.error('FileMoveToFolderError: {}'.format(e))

    def upload_image_to_drive(self, image_path):
        try:
            file_metadata = {
                'name': image_path,
                'parents': [self.folder_id]
            }


            Logger.debug('src/export/google_slides.py/upload_image_to_drive: Uploading image with path' + image_path)
            media = MediaFileUpload(image_path, mimetype='image/png')
            file = self.drive_service.files().create(body=file_metadata,
                                               media_body=media,
                                               fields='id, webContentLink').execute()

            Logger.debug('src/export/google_slides.py/upload_image_to_drive: Changing permissions for image with id' + file.get('id'))
            permissions = {
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'
            }
            self.drive_service.permissions().create(fileId=file.get('id'), body=permissions).execute()

            return file.get('webContentLink')
        except HttpError as e:
            Logger.error('ImageUploadError: {}'.format(e))


    def get_credentials(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        token_path = "src/export/token.json"
        creds = self.creds
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'src/export/credentials.json', SCOPES)
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

    def upload_image(self, image_path):
        try:
            if app_config.IMAGE_STORAGE_SERVICE == "GoogleDrive":
                image_id = self.upload_image_to_drive(image_path)
                return image_id
            elif app_config.IMAGE_STORAGE_SERVICE == "Imgur":
                uploaded_image = self.imgur_client.upload_from_path(image_path, config=None, anon=True)
                return uploaded_image['link']
            else:
                raise Exception("Invalid image storage service")
        except Exception as e:
            Logger.error("UploadImageError: {}".format(e))


    def insert_images(self, presentation_id):
        for image in self.images:
            try:

                uploaded_image_url = self.upload_image('sessions/'+ self.current_session + image.url)
                requests = [
                    {
                        'createImage': {
                            'url': uploaded_image_url,
                            'elementProperties': {
                                'pageObjectId': 'pageId' + str(self.images.index(image) + 1),
                                'size': {
                                    'height': {
                                        'magnitude': 200,
                                        'unit': 'PT'
                                    },
                                    'width': {
                                        'magnitude': 200,
                                        'unit': 'PT'
                                    }
                                },
                                'transform': {
                                    'scaleX': 1,
                                    'scaleY': 1,
                                    'translateX': 35,
                                    'translateY': 185,
                                    'unit': 'PT'
                                }
                            }
                        }
                    }
                ]
                self.send_batch_update(presentation_id, requests)
                Logger.info("Inserted image: " + image.url)
            except HttpError as err:
                Logger.error("Image insertion failed")
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
        # Open the markdown file
        with open(self.path, 'r', encoding='utf-8') as f:
            content = f.read()
            doc = panflute.convert_text(content, input_format='markdown')
        images = []
        paras = {}
        Logger.debug('Markdown: Getting titles and paragraphs')
        for elem in doc:
            if isinstance(elem, panflute.Header) and elem.level == 1:
                self.title = parse_text(elem)
                last_header = elem
            elif isinstance(elem, panflute.Header):
                last_header = elem
            elif isinstance(elem, panflute.Para):
                if isinstance(elem.content.__getitem__(0), panflute.Image):
                    images.append(elem.content.__getitem__(0))
                else:
                    paras[last_header] = paras.get(last_header, []) + [elem]
            elif isinstance(elem, panflute.Image):
                images.append(elem)
        self.paras = paras
        self.images = images