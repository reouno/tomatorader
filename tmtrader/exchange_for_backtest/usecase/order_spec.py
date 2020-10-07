from abc import ABC, abstractmethod
from typing import List

from tmtrader.entity.order import BasicOrder


class OrderSpec(ABC):
    @abstractmethod
    def filter(self, orders: List[BasicOrder]):
        pass
