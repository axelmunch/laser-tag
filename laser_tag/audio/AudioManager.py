from ..events.EventInstance import EventInstance


class AudioManager:
    """Audio manager"""

    def __init__(self):
        self.audio = None

    def set_audio_player(self, audio):
        self.audio = audio

    def update(self, events: list[EventInstance] = []):
        if self.audio is not None:
            self.audio.update(events)
