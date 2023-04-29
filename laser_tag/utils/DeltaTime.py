from time import time

from ..configuration import TARGET_FPS


class DeltaTime:
    __instances = {}

    def __new__(cls, id=None):
        if not id in cls.__instances:
            cls.__instances[id] = super().__new__(cls)
            cls.__instances[id].id = id
            cls.__instances[id].reset()
        return cls.__instances[id]

    def reset(self, current_time=None):
        if current_time is None:
            self.previous_time = time()
        else:
            self.previous_time = current_time
        self.current_time = self.previous_time
        self.dt = 0
        self.dt_target = 0

    def update(self, current_time=None):
        if current_time is None:
            self.current_time = time()
        else:
            self.current_time = current_time
        self.dt = self.current_time - self.previous_time
        self.dt_target = self.dt * TARGET_FPS
        self.previous_time = self.current_time

    def get_dt(self) -> float:
        return self.dt

    def get_dt_target(self) -> float:
        return self.dt_target
