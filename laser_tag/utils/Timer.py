from time import time


class Timer:
    """A simple timer class to measure time"""

    def __init__(self):
        self.timer_start = None
        self.timer_end = None

    def start(self):
        self.timer_start = time()

    def stop(self):
        self.timer_end = time()

    def get_time(self) -> float:
        return self.timer_end - self.timer_start
