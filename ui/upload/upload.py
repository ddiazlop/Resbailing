import os
from threading import Thread

import i18n
import src.utils.strategies.StrategyGuesser as StrategyGuesser

from kivy import Logger
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition
from plyer import filechooser

from ui.media.sound.utils import Soundmanager
from ui.superclasses.RelativeLayoutScreen import RelativeLayoutScreen


class UploadScreen(RelativeLayoutScreen):
    def __init__(self, main_app, **kwargs):
        super(UploadScreen, self).__init__(main_app, 'ui/upload/upload.kv', **kwargs)
        self.cols = 1

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, *args):
        Logger.debug('Resbailing: Loading dialog')
        # There is a bug (?) in filechooser that changes the current working directory
        # to the directory of the file that is selected. This is a workaround.
        curr_dir = os.getcwd()
        path = filechooser.open_file(title='Selecciona tu documento .md', filters=[('markdown files', '*.md')])
        os.chdir(curr_dir)
        if path:
            self.load(path)

    def load(self, path):
        # self.loading_view() #TODO: This is not working

        self.loading_view()
        Thread(target=self.summarize, args=(path[0],)).start()
        # Clock.schedule_once_free(lambda dt: self.summarize(path[0]))

    def select_session(self, session_name, *args):
        Logger.debug('Resbailing: Selecting session')
        self.main_app.session_manager.set_current_session(session_name)
        self.dismiss_popup()
        self.redirect_to_export()

    def show_select_session_popup(self, *args):
        Logger.debug('Resbailing: Prompting the user to select a session')
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        for session in self.main_app.session_manager.session_names:
            btn = Button(text=session, size_hint_y=None, height=40)
            btn.bind(on_release=lambda button: self.select_session(button.text))
            content.add_widget(btn)

        self._popup = Popup(title=i18n.t('dict.select_session'), content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def redirect_to_export(self, *args):
        Logger.debug('Resbailing: Redirecting to export')
        Soundmanager.play_done_sound()
        self.main_app.loading_screen.redirect_to('Export')

    def summarize(self, path):
        Logger.debug('Resbailing: Summarizing')
        loading_screen = self.main_app.loading_screen

        summarizer = StrategyGuesser.guess_summarization_strategy(path, loading_screen, generate_images=False) # TODO: Make this configurable
        summarizer.summarize()
        self.main_app.session_manager.select_last_session()
        # Redirect to export screen
        loading_screen.next_redirect = 'Export'
        loading_screen.redirect = True

    def loading_view(self, *args):
        Logger.debug('Resbailing: Loading view')
        self.main_app.screen_manager.transition = FadeTransition(duration=0.2)
        self.change_screen('Loading')
