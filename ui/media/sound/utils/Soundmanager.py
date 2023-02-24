from kivy.core.audio import SoundLoader


def play_done_sound():
    sound = SoundLoader.load('ui/media/sound/done_sound.wav')
    sound.volume = 1
    sound.play()
