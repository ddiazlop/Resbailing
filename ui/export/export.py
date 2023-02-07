import os

from kivy import Logger
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from src.export.google_slides import GoogleSlides

class ExportScreen(RelativeLayout):
    def __init__(self, **kwargs):
        Builder.load_file('ui/export/export.kv')
        super(ExportScreen, self).__init__(**kwargs)


    def export(self, *args):
        Logger.debug('ui/export/export.py: Exporting to Google Slides')
        # Get last session's markdown file.
        sessions = os.listdir('sessions')
        sessions.sort()
        last_session = sessions[-1]


        # Export to Google Slides
        slides = GoogleSlides(session_path="sessions/" + last_session)
        slides.export()



