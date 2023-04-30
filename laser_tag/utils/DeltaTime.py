from time import time

from ..configuration import TARGET_FPS


class DeltaTime:
    """Keep track of elapsed time between updates"""

    __instances = {}

    def __new__(cls, id=None):
        if not id in cls.__instances:
            cls.__instances[id] = super().__new__(cls)
            cls.__instances[id].id = id
            cls.__instances[id].reset()
        return cls.__instances[id]

    def reset(self, current_time: float = None):
        if current_time is None:
            self.previous_time = time()
        else:
            self.previous_time = current_time
        self.current_time = self.previous_time
        self.set_dt(0)

    def update(self, current_time: float = None):
        if current_time is None:
            self.current_time = time()
        else:
            self.current_time = current_time
        self.set_dt(self.current_time - self.previous_time)
        self.previous_time = self.current_time

    def set_dt(self, dt: float):
        self.dt = dt
        self.dt_target = dt * TARGET_FPS

    def get_dt(self) -> float:
        return self.dt

    def get_dt_target(self) -> float:
        return self.dt_target
