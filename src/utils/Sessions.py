import os
import re

import app_config


def get_session_md_path(session_name):
    return app_config.SESSIONS_PATH + '/' + session_name + '/presentation.md'


def get_session_names():
    date_regex = r'\.\/sessions\/\d{4}-\d{2}-\d{2}(-en)?$'
    sessions_list = [x[0].replace('./sessions/', '') for x in os.walk(app_config.SESSIONS_PATH) if
                     re.match(date_regex, x[0])]
    sessions_list.sort()
    return sessions_list


class SessionManager:
    def __init__(self):
        self.session_names = get_session_names()
        self.current_session_name = None
        self.current_session_md = None

    def set_current_session(self, session_name):
        self.current_session_name = session_name
        self.current_session_md = get_session_md_path(session_name)

    def select_last_session(self):
        self.set_current_session(self.get_last_session())

    def get_last_session(self):
        return self.session_names[-1]

    def is_session_selected(self):
        return self.current_session_name is not None
