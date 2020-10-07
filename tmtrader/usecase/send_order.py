from abc import ABC, abstractmethod
from typing import List

from tmtrader.entity.order import BasicOrder


class OrderObserver(ABC):
    @abstractmethod
    def notify_new_orders(self, orders: List[BasicOrder]):
        pass


class OrderSender(ABC):
    def __init__(self):
        self.__order_observers: List[OrderObserver] = list()

    def add_order_observer(self, observer: OrderObserver):
        self.__order_observers.append(observer)

    def remove_order_observer(self, observer: OrderObserver):
        self.__order_observers.remove(observer)

    def _notify_new_orders(self, orders: List[BasicOrder]):
        [obs.notify_new_orders(orders) for obs in self.__order_observers]
