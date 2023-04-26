from time import time

from ..configuration import TARGET_FPS


class DeltaTime:
    __instances = {}

    def __new__(cls, id=None):
        if not id in cls.__instances:
            cls.__instances[id] = super().__new__(cls)
        return cls.__instances[id]

    def __init__(self, id=None):
        self.id = id
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

    def get_dt(self) -> float:
        return self.dt

    def get_dt_target(self) -> float:
        return self.dt_target
