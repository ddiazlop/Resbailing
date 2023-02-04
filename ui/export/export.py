import os

from kivy import Logger
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from src.export.google_slides import create_presentation

class ExportScreen(RelativeLayout):
    def __init__(self, **kwargs):
        Builder.load_file('ui/export/export.kv')
        super(ExportScreen, self).__init__(**kwargs)


    def export(self, *args):
        Logger.debug('ui/export/export.py: Exporting to Google Slides')
        # Change curr dir to export dir
        curr_dir = os.getcwd()
        os.chdir('src/export')
        create_presentation("test")
        os.chdir(curr_dir)
