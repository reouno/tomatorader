from abc import ABC, abstractmethod
from typing import List

from tmtrader.entity.order import FilledOrder, Order


class OrderCloseObserver(ABC):
    @abstractmethod
    def notify_order_filled(self, order: FilledOrder):
        pass

    @abstractmethod
    def notify_order_cancelled(self, order: Order):
        pass


class OrderCloseNotifier(ABC):
    def __init__(self):
        self.__order_close_observers: List[OrderCloseObserver] = list()

    def add_order_close_observer(self, observer: OrderCloseObserver):
        self.__order_close_observers.append(observer)

    def remove_order_close_observer(self, observer: OrderCloseObserver):
        self.__order_close_observers.remove(observer)

    def _notify_order_filled(self, order: FilledOrder):
        [o.notify_order_filled(order) for o in self.__order_close_observers]

    def _notify_order_cancelled(self, order: Order):
        [o.notify_order_cancelled(order) for o in self.__order_close_observers]
