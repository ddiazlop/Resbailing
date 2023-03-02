import os
import sys

from kivy.config import Config
# Config.set('kivy', 'kivy_clock', 'free_all')
from kivy.resources import resource_add_path

import app_config
import i18n
from ui.main import Main




if __name__ == '__main__':
    # If python is running in debug mode, enable kivy's debug mode
    if app_config.DEBUG: Config.set('kivy', 'log_level', 'debug')
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    # Load internazionalization
    i18n.load_path.append(app_config.BASE_PATH + '/ui/i18n')
    i18n.set('locale', app_config.LANGUAGE)

    # Load main app
    main_app = Main()
    main_app.run()
