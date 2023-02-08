from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

from ui.superclasses.RelativeLayoutScreen import RelativeLayoutScreen


class ExportSuccessScreen(RelativeLayoutScreen):
    def __init__(self, main_app, **kwargs):
        super().__init__(main_app, 'ui/export/export_success.kv', **kwargs)

