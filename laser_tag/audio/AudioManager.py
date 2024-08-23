from ..events.EventInstance import EventInstance
from ..math.Point import Point


class AudioManager:
    """Audio manager"""

    def __init__(self):
        self.audio = None

    def set_audio_player(self, audio):
        self.audio = audio

    def set_listening_position(self, position: Point):
        if self.audio is not None:
            self.audio.set_listening_position(position)

    def update(self, events: list[EventInstance] = []):
        if self.audio is not None:
            self.audio.update(events)
