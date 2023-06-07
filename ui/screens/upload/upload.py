import os
from threading import Thread

import src.summarizer.strategies.utils.StrategyGuesser as StrategyGuesser

from kivy import Logger
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition
from plyer import filechooser

from ui.utils import Soundmanager
from src.i18n.Translator import t as _
from ui.screens.__superclasses.RelativeLayoutScreen import RelativeLayoutScreen


class UploadScreen(RelativeLayoutScreen):
    def __init__(self, main_app, **kwargs):
        super(UploadScreen, self).__init__(main_app, 'ui/screens/upload/upload.kv', **kwargs)
        self.cols = 1
        self.render_images = False
        self._popup = None

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        Logger.debug('Resbailing: Loading dialog')
        # There is a bug (?) in filechooser that changes the current working directory
        # to the directory of the file that is selected. This is a workaround.
        curr_dir = os.getcwd()
        path = filechooser.open_file(title='Selecciona tu documento .md', filters=[('md, mp3, wav', '*.md', '*.mp3', '*.wav')])
        os.chdir(curr_dir)
        if path:
            self.load(path)

    def set_render_images(self, value: bool):
        self.render_images = value
        self.dismiss_popup()
        self.show_load()

    def popup_want_images(self):
        """Shows a popup to the user to ask if he wants to generate images for the presentation"""
        Logger.debug('Resbailing: Prompting the user to generate images')
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        btn = Button(text=_('upload.yes'), size_hint_y=None, height=40)
        btn.bind(on_release=lambda button: self.set_render_images(True))
        content.add_widget(btn)
        btn = Button(text=_('upload.no'), size_hint_y=None, height=40)
        btn.bind(on_release=lambda button: self.set_render_images(False))
        content.add_widget(btn)

        self._popup = Popup(title=_('upload.want_images'), content=content,
                            size_hint=(0.6, 0.3))
        self._popup.open()

    def load(self, path):
        self.loading_view()
        Thread(target=self.summarize, args=(path[0],)).start()

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

        self._popup = Popup(title=_('upload.select_session'), content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def redirect_to_export(self, *args):
        Logger.debug('Resbailing: Redirecting to export')
        Soundmanager.play_done_sound()
        self.main_app.loading_screen.redirect_to('Export')

    def summarize(self, path):
        Logger.debug('Resbailing: Summarizing')
        loading_screen = self.main_app.loading_screen

        try:
            summarizer = StrategyGuesser.guess_summarization_strategy2(path, loading_screen, generate_images=self.render_images)
            summarizer.summarize()
            self.main_app.session_manager.select_last_session()
            # Redirect to export screen
            loading_screen.next_redirect = 'Export'
            loading_screen.redirect = True
        except Exception as e:
            loading_screen.show_error_dialog(e)

    def loading_view(self, *args):
        Logger.debug('Resbailing: Loading view')
        self.main_app.screen_manager.transition = FadeTransition(duration=0.2)
        self.change_screen('Loading')
