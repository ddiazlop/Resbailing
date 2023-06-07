import os
import sys

from kivy import Logger
from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, SlideTransition, FadeTransition, ScreenManager

from AppConfig import app_config
from src.i18n.Translator import t as _
from src.sessions.Sessions import SessionManager
from ui.screens.export.export import ExportScreen
from ui.screens.export.export_success import ExportSuccessScreen
from ui.screens.loading.loading import LoadingScreen
from ui.utils import Soundmanager
from ui.screens.settings.settings import SettingsScreen
from ui.screens.upload.upload import UploadScreen


class MainScreen(FloatLayout):
    def __init__(self, main_app, **kwargs):
        Soundmanager.play_done_sound()
        self.main_app = main_app
        super(MainScreen, self).__init__(**kwargs)

    def create_dropdown(self):
        dropdown = DropDown()
        for index, screen in enumerate(self.main_app.screen_manager.screens):
            btn = Button(text=screen.name, size_hint_y=None, height=35)
            btn.bind(on_release=lambda button: self.change_screen(button.text))
            dropdown.add_widget(btn)

        mainbutton = Button(text='Debug', size_hint=(None, None))
        mainbutton.bind(on_release=dropdown.open)
        mainbutton.pos_hint = {'top': 0.5, 'right': 0.6}
        self.add_widget(mainbutton)
        Logger.debug('Resbailing: Created dropdown')

    def pressed_button(self, button):
        if app_config.debug:  # Only create the dropdown if in debug mode
            self.create_dropdown()
        else:
            button.text = _('main.lets_go')

    def released_button(self, widget, *args):
        # Define the animation
        anim = Animation(background_color=(0, 1, 0, 1), duration=0.5)
        # Change the text of the button
        widget.text = _('main.ready_to_slide')

        anim.start(widget)

        anim.bind(on_complete=self.redirect_to_upload)

    def redirect_to_upload(self, *args):
        Logger.debug('Resbailing: Redirecting to upload')
        self.main_app.screen_manager.transition = SlideTransition(direction='down', duration=0.5)
        self.main_app.screen_manager.current = 'Upload'

    def change_screen(self, screen_name):
        Logger.debug('Resbailing: Changing screen to ' + screen_name)
        self.main_app.screen_manager.transition = FadeTransition(duration=0.2)
        self.main_app.screen_manager.current = screen_name

    def show_settings(self):
        Logger.debug('Resbailing: Showing settings')
        self.main_app.screen_manager.transition = FadeTransition(duration=0.2)
        self.main_app.screen_manager.current = 'Settings'

    def unload(self):
        self.main_app.screen_manager.remove_widget(self)
        Builder.unload_file(self.kv_file_loc)

class Main(App):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.session_manager = None
        self.screen_manager = None
        self.main_screen = None
        self.upload_screen = None
        self.export_screen = None
        self.export_success_screen = None
        self.loading_screen = None
        self.settings_screen = None

    def build(self):
        self.icon = 'ui/media/icons/resbanoback.png'
        self.title = 'Resbailing'

        self.session_manager = SessionManager()
        self.screen_manager = ScreenManager()

        self.main_screen = MainScreen(main_app=self)
        screen = Screen(name='Main')
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)

        self.upload_screen = UploadScreen(main_app=self)
        screen = Screen(name='Upload')
        screen.add_widget(self.upload_screen)
        self.screen_manager.add_widget(screen)

        self.export_screen = ExportScreen(main_app=self)
        screen = Screen(name='Export')
        screen.add_widget(self.export_screen)
        self.screen_manager.add_widget(screen)

        self.export_success_screen = ExportSuccessScreen(main_app=self)
        screen = Screen(name='ExportSuccess')
        screen.add_widget(self.export_success_screen)
        self.screen_manager.add_widget(screen)

        self.loading_screen = LoadingScreen(main_app=self)
        screen = Screen(name='Loading')
        screen.add_widget(self.loading_screen)
        self.screen_manager.add_widget(screen)

        self.settings_screen = SettingsScreen(main_app=self)
        screen = Screen(name='Settings')
        screen.add_widget(self.settings_screen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    @staticmethod
    def restart():
        Logger.debug('Resbailing: Restarting app')
        os.execl(sys.executable, 'index.py', *sys.argv)

    @staticmethod
    def exit():
        Logger.debug('Resbailing: Exiting app')
        sys.exit()