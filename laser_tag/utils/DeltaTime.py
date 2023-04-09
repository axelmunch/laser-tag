from time import time

from ..configuration import TARGET_FPS


class DeltaTime:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(DeltaTime, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.reset()

    def reset(self):
        self.previous_time = time()
        self.current_time = self.previous_time
        self.dt = 0
        self.dt_target = 0

    def update(self):
        self.current_time = time()
        self.dt = self.current_time - self.previous_time
        self.dt_target = self.dt * TARGET_FPS
        self.previous_time = self.current_time

    def get_dt(self):
        return self.dt

    def get_dt_target(self):
        return self.dt_target
