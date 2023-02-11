import os

from kivy import Logger
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import FadeTransition
from plyer import filechooser

from src.readers.pdf import PdfAnalyzer
from src.readers.markdown import MarkdownSummarizer
from ui.media.sound.utils import Soundmanager
from ui.superclasses.RelativeLayoutScreen import RelativeLayoutScreen


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class UploadScreen(RelativeLayoutScreen):
    def __init__(self,main_app, **kwargs):
        super(UploadScreen, self).__init__(main_app,'ui/upload/upload.kv',**kwargs)
        self.cols = 1

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, *args):
        Logger.debug('ui/upload/upload.py: Loading dialog')
        # There is a bug (?) in filechooser that changes the current working directory
        # to the directory of the file that is selected. This is a workaround.
        curr_dir = os.getcwd()
        Clock.schedule_once(self.loading_view)
        path = filechooser.open_file(title='Selecciona tu documento .md', filters=[('markdown files', '*.md')])
        os.chdir(curr_dir)

        self.loading_view()
        Clock.schedule_once(lambda dt: self.summarize(path[0]))

        i = 0

    def redirect_to_export(self, *args):
        Logger.debug('ui/upload/upload.py: Redirecting to export')
        Soundmanager.play_done_sound()
        self.main_app.screen_manager.transition = FadeTransition(duration=0.2)
        self.change_screen('Export')

    def summarize(self, path):
        Logger.debug('ui/upload/upload.py: Summarizing')
        summarizer = MarkdownSummarizer(path)
        summarizer.summarize()
        # Redirect to export screen
        self.redirect_to_export()


    def loading_view(self, *args):
        Logger.debug('ui/upload/upload.py: Loading view')
        self.remove_widget(self.ids.upload)
        self.add_widget(GridLayout(cols=1))

        self.add_widget(Image(source='ui/media/images/upload/loading.gif'))
        self.add_widget(Label(text="Cargando..."))





