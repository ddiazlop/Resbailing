from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from kivy import Logger
from config import GOOGLE_SCOPES as SCOPES


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_presentation(title):
    creds = get_credentials()
    try:
        service = build('slides', 'v1', credentials=creds)
        body = {
            'title': title
        }
        presentation = service.presentations().create(body=body).execute()
        Logger.info("Presentation created: " + presentation.get('presentationId'))
        return presentation
    except HttpError as err:
        Logger.error("Presentation creation failed")
        Logger.error("Error code: " + err.resp.status)
        Logger.error("Error message: " + err.resp.reason)