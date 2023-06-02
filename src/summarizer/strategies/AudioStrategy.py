import os

from kivy import Logger
from pydub.silence import split_on_silence

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import librosa

from pydub import AudioSegment

from AppConfig import app_config
from src.summarizer.strategies.NoFormatStrategy import NoFormatStrategy

from src.i18n.Translator import t as _


class AudioStrategy(NoFormatStrategy):
    """
    This class is responsible for reading the audio file and creating the slides for it.
    Its main difference from the NoFormatStrategy is that it does not use the text, but instead
    the audio file to generate the slides.

    Inputting an audio file does not change the way the slides are generated, but it does change
    the way the slides are read.
    """
    def __init__(self, path, loading_screen, generate_image: bool = True):
        super().__init__(path, loading_screen, generate_image)
        Logger.debug('Resbailing: Using AudioStrategy')
        if app_config.language == 'en':
            self.locale = 'en-US'
        elif app_config.language == 'es':
            self.locale = 'es-ES'
        else:
            raise ValueError('Language not supported')


        self.update_loading_info(_('loading.loading_audio_model'))
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")



    @staticmethod
    def check_input(values, **kwargs):
        filename = kwargs['filename']
        return filename.endswith('.mp3') or filename.endswith('.wav')

    def read_lines(self):
        """
        Listens for the audio file and returns the text.
        :return:
        """
        self.update_loading_info(_('loading.reading_audio'))
        path = self.path.replace('\\', '/')

        # We need the file to be in .wav format
        if self.path.endswith('.mp3'):
            sound = AudioSegment.from_mp3(path)
            path = self.writer.session_path + "/audio/audio.wav"
            sound.export(path, format='wav')

        self.update_loading_info(_('loading.analyzing_audio'))

        text = self.get_audio_transcription(path)
        # End of difference

        return self.extract_sentences(text)

    def get_audio_transcription(self, path):
        """
        Uses the Wav2Vec2 model to transcribe the audio file.
        :param path:
        :return:
        """
        sound = AudioSegment.from_wav(path)
        chunks = split_on_silence(sound,
                                  min_silence_len=500,
                                  # adjust this per requirement
                                  silence_thresh=sound.dBFS - 14,
                                  # keep the silence for 1 second, adjustable as well
                                  keep_silence=500,
                                  )
        folder_name = self.writer.session_path + "/audio"
        whole_text = ""
        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")

            # Load audio
            Logger.debug('Resbailing: Loading audio ' + chunk_filename)
            whole_text += self.get_native_transcription(chunk_filename, whole_text)

        return whole_text

    def get_native_transcription(self, chunk_filename, whole_text):
        """
        Uses the native Wav2Vec2 model to transcribe the audio file.
        :param chunk_filename:
        :param whole_text:
        :return:
        """
        audio_input, _ = librosa.load(chunk_filename, sr=16000)
        input_values = self.processor(audio_input, return_tensors="pt", padding="longest").input_values
        # Get logits
        with torch.no_grad():
            logits = self.model(input_values).logits
        # Decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        whole_text += self.cleaner.style_sentence(transcription)
        return whole_text


