from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout


class RelativeLayoutScreen(RelativeLayout):
    def __init__(self, main_app, kv_file_loc, **kwargs):
        self.main_app = main_app
        Builder.load_file(kv_file_loc)
        super(RelativeLayoutScreen, self).__init__(**kwargs)

    def change_screen(self, screen_name):
        self.main_app.screen_manager.current = screen_name

    def unload(self):
        self.main_app.screen_manager.remove_widget(self)
        Builder.unload_file(self.kv_file_loc)

class BoxLayoutScreen(BoxLayout):
    def __init__(self, main_app, kv_file_loc, **kwargs):
        self.main_app = main_app
        Builder.load_file(kv_file_loc)
        self.kv_file_loc = kv_file_loc
        super(BoxLayoutScreen, self).__init__(**kwargs)

    def change_screen(self, screen_name):
        self.main_app.screen_manager.current = screen_name

    def unload(self):
        self.main_app.screen_manager.remove_widget(self)
        Builder.unload_file(self.kv_file_loc)
