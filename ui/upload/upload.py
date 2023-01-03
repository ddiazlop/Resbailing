import os
from tkinter.ttk import Button

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from plyer import filechooser
import PyPDF2

from src.readers.pdf import DocumentData


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class UploadScreen(RelativeLayout):
    def __init__(self, **kwargs):
        Builder.load_file('ui/upload/upload.kv')
        super(UploadScreen, self).__init__(**kwargs)
        self.cols = 1

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, *args):
        print('Loading dialog')
        path = filechooser.open_file(title='Selecciona tu documento PDF', filters=[('PDF files', '*.pdf')])
        print('Reading PDF')
        data = DocumentData(path[0])
        i = 0
        # self.load = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        # self._popup = Popup(title="Load file", content=self.load, size_hint=(0.9, 0.9))
        # self._popup.open()

    def load(self, path, filename):
        print('Loading file')
        with open(os.path.join(path, filename[0])) as stream:
            self.ids.upload.text = stream.read()

        self.dismiss_popup()


