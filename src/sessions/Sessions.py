import datetime
import os
import re
import shutil

from AppConfig import app_config


def get_session_md_path(session_name):
    return app_config.sessions_path + '/' + session_name + '/presentation.md'


def get_session_names():
    date_regex = r'^\d{4}-\d{2}-\d{2}(?:_\d+)?$'
    sessions_list = []

    if not os.path.exists(app_config.sessions_path):
        os.mkdir(app_config.sessions_path)

    for session in os.listdir(app_config.sessions_path):
        session = session.replace(app_config.sessions_path, '')
        content = os.listdir(app_config.sessions_path + '/' + session)
        if re.match(date_regex, session) and 'presentation.md' in content:
            sessions_list.append(session)
        else:
            shutil.rmtree(app_config.sessions_path + '/' + session)


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
        self.session_names = get_session_names()
        self.set_current_session(self.get_last_session())

    def get_last_session(self):
        return self.session_names[-1]

    def is_session_selected(self):
        return self.current_session_name is not None
