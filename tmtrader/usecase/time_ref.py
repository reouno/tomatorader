import time
from abc import ABC, abstractmethod


class TimeRef(ABC):
    @abstractmethod
    def now(self) -> float:
        pass


class DefaultTimeRef(TimeRef):
    def now(self) -> float:
        return time.time()
