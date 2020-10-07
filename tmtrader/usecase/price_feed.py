from abc import ABC, abstractmethod

from tmtrader.entity.price import PriceSequence


class PriceObserver(ABC):
    @abstractmethod
    def notify_price_update(self, price_ref: PriceSequence):
        pass


class PriceFeeder(ABC):
    def __init__(self):
        self.__observers = list()

    def add_price_observer(self, obs: PriceObserver):
        self.__observers.append(obs)

    def remove_price_observer(self, obs: PriceObserver):
        self.__observers.remove(obs)

    def _notify_price_update(self, price_sequence_ref: PriceSequence):
        [obs.notify_price_update(price_sequence_ref) for obs in
         self.__observers]
