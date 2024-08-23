import pygame

from ..configuration import AUDIO_CHANNELS, MUSIC_FADEOUT_MS, VARIABLES
from ..events.Event import Event
from ..events.EventInstance import EventInstance
from ..math.distance import distance_points
from ..math.Point import Point
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

        self.listening_position = Point(0, 0)

        self.latest_global_volume = 0
        self.latest_music_volume = 0
        self.latest_effects_volume = 0

    def load_sound(self, audio: Audio, path):
        self.sounds[audio] = pygame.mixer.Sound(path)

    def play_sound(self, audio: Audio, position=None):
        channel = pygame.mixer.Channel(
            self.channel_index % (pygame.mixer.get_num_channels() - 1)
        )

        if position is None:
            channel.set_volume(1)
        else:
            # Distance multiplier
            distance_multiplier = min(
                1, max(0, 1 - (distance_points(self.listening_position, position) / 20))
            )

            channel.set_volume(distance_multiplier)

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

    def set_listening_position(self, position: Point):
        self.listening_position = position

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
                position = None
                if isinstance(event.data, list) and len(event.data) == 2:
                    audio = event.data[0]
                    position = Point.create(event.data[1])
                try:
                    audio = Audio(audio)
                except ValueError:
                    pass

                if audio in music_audio:
                    self.play_music(audio)
                else:
                    self.play_sound(audio, position=position)

        if self.transition_music is not None:
            channel = pygame.mixer.Channel(pygame.mixer.get_num_channels() - 1)
            # Replace the music if the channel is free
            if not channel.get_busy():
                channel.play(
                    self.sounds[self.transition_music],
                    loops=-1 if self.transition_music in loop_audio else 0,
                )
                self.transition_music = None
