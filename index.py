import os
import sys

from kivy.config import Config
from kivy.resources import resource_add_path

import app_config
from ui.main import Main

if __name__ == '__main__':
    # If python is running in debug mode, enable kivy's debug mode
    if app_config.DEBUG: Config.set('kivy', 'log_level', 'debug')
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    main_app = Main()
    main_app.run()
