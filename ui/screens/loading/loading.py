from kivy.clock import Clock
from kivy.uix.screenmanager import FadeTransition

from ui.utils.superclasses.RelativeLayoutScreen import RelativeLayoutScreen




class LoadingScreen(RelativeLayoutScreen):

    def __init__(self, main_app, **kwargs):
        super(LoadingScreen, self).__init__(main_app, 'ui/screens/loading/loading.kv', **kwargs)
        self.cols = 1
        self.progress = 0
        self.progress_max = 0
        self.progress_value = 0
        self.next_redirect = None
        self.redirect = False
        self.waiting_event = Clock.schedule_interval(lambda dt: self.check_for_redirect(), 0.1)
        self.waiting()


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

    def update_info(self, info):
        Clock.schedule_once(lambda dt: self.change_info(info), -1)
        Clock.tick()







