import pygame

from ..configuration import AUDIO_CHANNELS, MUSIC_FADEOUT_MS, VARIABLES
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from .Audio import Audio, loop_audio, music_audio
from .AudioManager import AudioManager


class AudioPlayer(AudioManager):
    """Audio player"""

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)

            cls.__instance.init()

        return cls.__instance

    def init(self):
        pygame.mixer.init()

        pygame.mixer.set_num_channels(AUDIO_CHANNELS)

        self.sounds: dict[Audio, pygame.mixer.Sound] = {}

        self.channel_index = 0

        self.transition_music = None

        self.latest_global_volume = 0
        self.latest_music_volume = 0
        self.latest_effects_volume = 0

    def load_sound(self, audio: Audio, path):
        self.sounds[audio] = pygame.mixer.Sound(path)

    def play_sound(self, audio: Audio):
        channel = pygame.mixer.Channel(
            self.channel_index % (pygame.mixer.get_num_channels() - 1)
        )
        channel.play(self.sounds[audio])

        self.channel_index += 1

    def play_music(self, audio: Audio):
        self.transition_music = audio
        channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
        channel.fadeout(MUSIC_FADEOUT_MS)

    def update_volume(self):
        for audio, sound in self.sounds.items():
            if audio in music_audio:
                sound.set_volume(VARIABLES.volume_global * VARIABLES.volume_music)
            else:
                sound.set_volume(VARIABLES.volume_global * VARIABLES.volume_effects)

    def update(self, events: list[EventInstance] = []):
        if (
            VARIABLES.volume_global != self.latest_global_volume
            or VARIABLES.volume_music != self.latest_music_volume
            or VARIABLES.volume_effects != self.latest_effects_volume
        ):
            self.latest_global_volume = VARIABLES.volume_global
            self.latest_music_volume = VARIABLES.volume_music
            self.latest_effects_volume = VARIABLES.volume_effects

            self.update_volume()

        for event in events:
            if event.id in [Event.PLAY_SOUND, Event.PLAY_SOUND_LOCAL]:
                audio = event.data
                try:
                    audio = Audio(audio)
                except ValueError:
                    pass
                self.play_music(audio)

        if self.transition_music is not None:
            channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
            # Replace the music if the channel is free
            if not channel.get_busy():
                channel.play(
                    self.sounds[self.transition_music],
                    loops=-1 if self.transition_music in loop_audio else 0,
                )
                self.transition_music = None
