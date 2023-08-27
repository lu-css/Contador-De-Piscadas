import pygame
import time
import threading

from pydub import AudioSegment
from pydub.playback import play

class AudioControll:
    def __init__(self, audios) -> None:
        self.audios = audios
        self.playing = False
        self.audio = None

    def _random(self):
        size = len(self.audios)
        if size == 0:
            return None

        return self.audios[size - 1]

    def play_random(self):
        audio_path = self._random()

        if not audio_path:
            print("Empty Audios")
            return

        if not self.playing:
            self.audio = audio_path
            thread = threading.Thread(target=self.play)
            print(f"PLAYING AUDIO {audio_path}")
            thread.start()

    def play(self):
        if not self.audio:
            return

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.play()
        self.playing = True

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        pygame.quit()
        self.playing = False
