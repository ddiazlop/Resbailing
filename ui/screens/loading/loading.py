from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition

from ui.screens.__superclasses.RelativeLayoutScreen import RelativeLayoutScreen
from src.i18n.Translator import t as _


class LoadingScreen(RelativeLayoutScreen):

    def __init__(self, main_app, **kwargs):
        super(LoadingScreen, self).__init__(main_app, 'ui/screens/loading/loading.kv', **kwargs)
        self.popup = None
        self.cols = 1
        self.progress = 0
        self.progress_max = 0
        self.progress_value = 0
        self.next_redirect = None
        self.redirect = False
        self.waiting_event = Clock.schedule_interval(lambda dt: self.check_for_redirect(), 0.1)
        self.waiting()


    @mainthread
    def show_error_dialog(self, exception: Exception):
        """Creates a popup showing the error message, and a button to restart the app."""
        self.popup = Popup(title="Error", size_hint=(None, None), size=(400, 200))
        layout = BoxLayout(orientation='vertical', padding=10)
        error_label = Label(text=str(exception), size_hint=(1, 0.8), halign='center', valign='middle',
                            text_size=(self.popup.width - 20, None), size=(self.popup.width - 20, self.popup.height * 0.6))
        error_label.bind(texture_size=error_label.setter('size'))
        layout.add_widget(error_label)
        restart_button = Button(text=_("export.restart"), size_hint=(1, 0.3))
        restart_button.bind(on_press=lambda x: self.main_app.restart())
        layout.add_widget(restart_button)
        self.popup.content = layout
        self.popup.open()

    def waiting(self):
        self.redirect = False
        self.waiting_event()

    def check_for_redirect(self, *args):
        if self.redirect:
            self.waiting_event.cancel()
            self.redirect_to_next()

    def redirect_to_next(self):
        self.main_app.screen_manager.transition = FadeTransition()
        self.main_app.screen_manager.current = self.next_redirect

    def set_redirect_destination(self, screen_name):
        self.next_redirect = screen_name
        self.waiting()


    def redirect_to(self, screen_name):
        self.next_redirect = screen_name
        self.waiting()
        self.redirect = True

    def change_info(self, info):
        self.ids.info.text = info

    @mainthread
    def update_info(self, info):
        Clock.schedule_once(lambda dt: self.change_info(info), -1)
        Clock.tick()







