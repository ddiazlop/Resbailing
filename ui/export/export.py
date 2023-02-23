import os

from kivy import Logger
from src.export.google_slides import GoogleSlides
from src.utils import Sessions
from ui.superclasses.RelativeLayoutScreen import RelativeLayoutScreen


class ExportScreen(RelativeLayoutScreen):
    def __init__(self, main_app, **kwargs):
        super(ExportScreen, self).__init__(main_app,'ui/export/export.kv', **kwargs)


    def export(self, *args):
        Logger.debug('ui/export/export.py: Exporting to Google Slides')

        # Export to Google Slides
        slides = GoogleSlides(self.main_app.session_manager)
        slides.export()
        self.change_screen('ExportSuccess')




