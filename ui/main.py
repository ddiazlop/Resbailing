from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition, FadeTransition, SlideTransition

from ui.upload.upload import UploadScreen

class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def pressed_button(self, widget, *args):
        # Define the animation
        anim = Animation(background_color=(0,1,0,1), duration=1.5)
        # Change the text of the button
        widget.text = '¿Preparado para deslizarte?'
        anim.start(widget)

        anim.bind(on_complete=self.redirect_to_upload)

    def redirect_to_upload(self, *args):
        print('Changing screen')
        main_app.screen_manager.transition = SlideTransition(direction='down', duration=2)
        main_app.screen_manager.current = 'Upload'


class Main(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_screen = MainScreen()
        screen = Screen(name='Main')
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)

        self.upload_screen = UploadScreen()
        screen = Screen(name='Upload')
        screen.add_widget(self.upload_screen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    main_app = Main()
    main_app.run()