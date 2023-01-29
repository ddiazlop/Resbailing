import os
import threading
from tkinter.ttk import Button

from kivy import Logger
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from plyer import filechooser

from src.readers.pdf import PdfAnalyzer



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
        Logger.debug('Upload: Loading dialog')
        # There is a bug (?) in filechooser that changes the current working directory
        # to the directory of the file that is selected. This is a workaround.
        curr_dir = os.getcwd()
        Clock.schedule_once(self.loading_view)
        path = filechooser.open_file(title='Selecciona tu documento PDF', filters=[('PDF files', '*.pdf')])
        os.chdir(curr_dir)

        self.loading_view()
        Clock.schedule_once(lambda dt: self.read_document(path))

        i = 0

    def read_document(self, path):
        Logger.debug('Upload: Trying to read PDF')
        analyzer = PdfAnalyzer(path[0])
        analyzer.full_analysis()


    def loading_view(self, *args):
        Logger.debug('Upload: Loading view')
        self.remove_widget(self.ids.upload)
        self.add_widget(GridLayout(cols=1))

        self.add_widget(Image(source='ui/images/upload/loading.gif'))
        self.add_widget(Label(text="Cargando..."))





