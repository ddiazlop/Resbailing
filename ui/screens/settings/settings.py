from ui.screens.__superclasses.RelativeLayoutScreen import BoxLayoutScreen
from AppConfig import app_config as cfg

class SettingsScreen(BoxLayoutScreen):
    def __init__(self, main_app, **kwargs):
        super(SettingsScreen, self).__init__(main_app, 'ui/screens/settings/settings.kv', **kwargs)
        self.cols = 1

    def apply_settings(self):
        cfg.save_config()
        self.main_app.restart()

    def cancel_settings(self):
        cfg.load_config()
        # Reset the settings screen
        self.ids['language_spinner'].text = cfg.language

        self.change_screen('Main')
