from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout


class RelativeLayoutScreen(RelativeLayout):
    def __init__(self, main_app, kv_file_loc, **kwargs):
        self.main_app = main_app
        Builder.load_file(kv_file_loc)
        super(RelativeLayoutScreen, self).__init__(**kwargs)

    def change_screen(self, screen_name):
        self.main_app.screen_manager.current = screen_name
