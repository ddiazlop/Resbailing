import os

from kivy import Logger
from src.export.google_slides import GoogleSlides
from ui.superclasses.RelativeLayoutScreen import RelativeLayoutScreen


class ExportScreen(RelativeLayoutScreen):
    def __init__(self, main_app, **kwargs):
        super(ExportScreen, self).__init__(main_app,'ui/export/export.kv', **kwargs)


    def export(self, *args):
        Logger.debug('ui/export/export.py: Exporting to Google Slides')
        # Get last session's markdown file.
        sessions = os.listdir('sessions')
        sessions.sort()
        last_session = sessions[-1]


        # Export to Google Slides
        slides = GoogleSlides(session_path="sessions/" + last_session)
        slides.export()
        self.change_screen('ExportSuccess')




