import os

from kivy import Logger
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition
from plyer import filechooser

from src.readers.markdown import MarkdownSummarizer
from src.utils.Sessions import get_session_md_path, get_session_names
from ui.export.export import ExportScreen
from ui.media.sound.utils import Soundmanager
from ui.superclasses.RelativeLayoutScreen import RelativeLayoutScreen


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
        path = filechooser.open_file(title='Selecciona tu documento .md', filters=[('markdown files', '*.md')])
        os.chdir(curr_dir)
        if path:
            self.load(path)

    def load(self, path):
        # self.loading_view() #TODO: This is not working
        Clock.schedule_once(lambda dt: self.loading_view())
        Clock.schedule_once(lambda dt: self.summarize(path[0]), 0.5)

    def select_session(self, session_name, *args):
        Logger.debug('ui/upload/upload.py: Selecting session')
        self.main_app.session_manager.set_current_session(session_name)
        self.dismiss_popup()
        self.redirect_to_export()

    def show_select_session_popup(self, *args):
        Logger.debug('ui/upload/upload.py: Prompting the user to select a session')
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        for session in self.main_app.session_manager.session_names:
            btn = Button(text=session, size_hint_y=None, height=40)
            btn.bind(on_release=lambda button: self.select_session(button.text))
            content.add_widget(btn)

        self._popup = Popup(title="Selecciona tu sesión", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()




    def redirect_to_export(self, *args):
        Logger.debug('ui/upload/upload.py: Redirecting to export')
        Soundmanager.play_done_sound()
        self.main_app.screen_manager.transition = FadeTransition(duration=0.2)
        self.change_screen('Export')

    def summarize(self, path):
        Logger.debug('ui/upload/upload.py: Summarizing')
        summarizer = MarkdownSummarizer(path)
        summarizer.summarize()
        self.main_app.session_manager.select_last_session()
        # Redirect to export screen
        self.redirect_to_export()


    def loading_view(self, *args):
        Logger.debug('ui/upload/upload.py: Loading view')
        self.remove_widget(self.ids.upload)
        self.add_widget(GridLayout(cols=1))

        self.add_widget(Image(source='ui/media/images/upload/loading.gif'))
        self.add_widget(Label(text="Cargando..."))





