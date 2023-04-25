from __future__ import print_function

import os.path
from time import sleep

import panflute
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from imgurpython import ImgurClient
from kivy import Logger

import app_config
from app_config import GOOGLE_SCOPES as SCOPES

from src.export.utils import RequestPicker
from src.export.creator.TitleRequestCreator import TitleRequestCreator
from src.utils.loggers import ErrorLogger
from src.utils.Docmdutils import parse_text
from src.i18n.Translator import t as _


def get_credentials(creds=None, update_loading_screen=None):
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_path = "src/export/credentials/token.json"
    try:
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if update_loading_screen:
                update_loading_screen(_('export.login_to_google'))
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'src/export/credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    except RefreshError:
        ErrorLogger.log_warning("Credentials refresh failed")
        Logger.info("ResbailingGoogleSlidesExport: Deleting token.json")
        os.remove(token_path)
        return get_credentials(update_loading_screen=update_loading_screen)


class GoogleSlides:
    def __init__(self, session_manager, loading_screen):
        self.loading_screen = loading_screen

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
        self.loading_screen.update_info(_('export.logged_in_google'))
        self.service = build('slides', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

        self.creator_memos = []


    def export(self):
        self.loading_screen.update_info(_('export.exporting_to_google_slides'))
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
                for g_file in response.get('files', []):
                    if g_file.get('name') == folder_name:
                        self.folder_id = g_file.get(
                            'id')
                        return
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            g_file = self.drive_service.files().create(body=file_metadata,
                                                     fields='id').execute()
            self.folder_id = g_file.get('id')
        except HttpError as e:
            ErrorLogger.log_error(e)

    def move_files_to_folder(self, file_id):
        try:
            g_file = self.drive_service.files().get(fileId=file_id,
                                                  fields='parents').execute()
            previous_parents = ",".join(g_file.get('parents'))
            g_file = self.drive_service.files().update(fileId=file_id,
                                                     addParents=self.folder_id,
                                                     removeParents=previous_parents,
                                                     fields='id, parents').execute()
            Logger.info(
                'FileMoveToFolderSuccess: Moved file with id' + g_file.get('id') + ' to folder with id' + self.folder_id)
        except HttpError as e:
            ErrorLogger.log_error(e)

    def upload_image_to_drive(self, image_path):
        try:
            file_metadata = {
                'name': image_path,
                'parents': [self.folder_id]
            }

            Logger.debug('Resbailing: Uploading image with path' + image_path)
            media = MediaFileUpload(image_path, mimetype='image/png')
            g_file = self.drive_service.files().create(body=file_metadata,
                                                     media_body=media,
                                                     fields='id, webContentLink').execute()

            Logger.debug(
                'Resbailing: Changing permissions for image with id' + g_file.get(
                    'id'))
            permissions = {
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'
            }
            self.drive_service.permissions().create(fileId=g_file.get('id'), body=permissions).execute()

            return g_file.get('webContentLink')
        except HttpError as e:
            ErrorLogger.log_error(e)

    def get_credentials(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        self.creds = get_credentials(update_loading_screen=self.loading_screen.update_info)

    def create_presentation(self):
        try:
            body = {
                'title': self.title
            }
            presentation = self.service.presentations().create(body=body).execute()
            self.set_title_slide(presentation.get('presentationId'))
            Logger.info("Resbailing: Presentation created -> " + presentation.get('presentationId'))
            return presentation
        except HttpError as err:
            ErrorLogger.log_error(err, "Presentation creation failed with error code -> " + str(err.resp.status) + " | "+ err.resp.reason)


    def set_title_slide(self, presentation_id):
        Logger.info("Resbailing: Creating title slide")
        self.loading_screen.update_info(_('loading.creating_title_slide'))

        creator = TitleRequestCreator(self.page_id, title=self.title)
        requests = creator.create_request()

        self.send_batch_update(presentation_id, requests)
        self.page_id += 1

    def create_slide(self, presentation_id, title, body):
        try:
            creator = RequestPicker.get_random_request_type(self.page_id, title=title, body=body)
            requests = creator.create_request()

            self.creator_memos.append(creator) # Save the creator to be able to add images later
            self.send_batch_update(presentation_id, requests)
            Logger.info("Resbailing: Created slide with ID -> " + 'pageId' + str(self.page_id))
            self.loading_screen.update_info(_('loading.creating_slide') + " " + str(self.page_id))
            self.page_id += 1
        except HttpError as err:
            ErrorLogger.log_error(err, "Slide creation failed with error code -> " + str(err.resp.status) + " | "+ err.resp.reason)

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
            ErrorLogger.log_error(e, "Image upload failed")

    def insert_images(self, presentation_id):
        for image in self.images:
            try:
                sleep(0.5) # To avoid rate limit
                self.loading_screen.update_info(_('export.inserting_image') + " " + image.url)
                uploaded_image_url = self.upload_image('sessions/' + self.current_session + image.url)
                index = self.images.index(image) + 1

                # Restores the creator used to create the slide.
                creator = self.creator_memos[index - 1]
                requests = creator.create_image_request(uploaded_image_url, index)

                self.send_batch_update(presentation_id, requests)
                Logger.info("Resbailing: Inserted image -> " + image.url)
            except HttpError as err:
                ErrorLogger.log_error(err, "Image insertion failed with error code -> " + str(err.resp.status) + " | "+ err.resp.reason)

    def send_batch_update(self, presentation_id, requests):
        try:
            body = {
                'requests': requests
            }

            response = self.service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()
            Logger.debug("Resbailing: Batch update response -> " + str(response))
            return response

        except HttpError as err:
            ErrorLogger.log_error(err, "Batch update failed with error code -> " + str(err.resp.status) + " | "+ err.resp.reason)

    def init_content(self):
        # Open the markdown file
        with open(self.path, 'r', encoding='utf-8') as f:
            content = f.read()
            doc = panflute.convert_text(content, input_format='markdown')
        images = []
        paras = {}
        Logger.debug('Resbailing: Getting titles and paragraphs')
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
