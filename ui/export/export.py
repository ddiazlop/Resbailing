from threading import Thread

from kivy import Logger
from kivy.uix.screenmanager import FadeTransition

from src.export.google_slides import GoogleSlides
from ui.superclasses.RelativeLayoutScreen import RelativeLayoutScreen


class ExportScreen(RelativeLayoutScreen):
    def __init__(self, main_app, **kwargs):
        super(ExportScreen, self).__init__(main_app, 'ui/export/export.kv', **kwargs)

    def export(self, *args):
        Logger.debug('Resbailing: Exporting to Google Slides')
        loading_screen = self.main_app.loading_screen

        # Export to Google Slides
        Thread(target=self.export_to_google_slides, args=(loading_screen,)).start()
        self.main_app.screen_manager.transition = FadeTransition(duration=0.2)
        loading_screen.set_redirect_destination('ExportSuccess')
        self.main_app.screen_manager.current = 'Loading'


    def export_to_google_slides(self, loading_screen):
        slides = GoogleSlides(self.main_app.session_manager, loading_screen)
        slides.export()
        self.main_app.loading_screen.redirect = True
