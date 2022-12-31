from tkinter.ttk import Button

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image


class UploadScreen(GridLayout):
    def __init__(self, **kwargs):
        Builder.load_file('ui/upload/upload.kv')
        super(UploadScreen, self).__init__(**kwargs)
        self.cols = 1


