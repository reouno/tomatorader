from abc import ABC, abstractmethod
from decimal import Decimal
from typing import NamedTuple

from tmtrader._typing import ArrayLike


class PriceSequence(ABC):
    """Stock price sequence
    Each sequence is ordered from the latest value to the oldest value.
    The oldest value can be configured at common properties that decide how
    many past bars to use.
    """

    @property
    @abstractmethod
    def _open(self):
        pass

    @_open.getter
    @abstractmethod
    def open(self) -> ArrayLike:
        pass

    @property
    @abstractmethod
    def _high(self):
        pass

    @_high.getter
    @abstractmethod
    def high(self) -> ArrayLike:
        pass

    @property
    @abstractmethod
    def _low(self):
        pass

    @_low.getter
    @abstractmethod
    def low(self) -> ArrayLike:
        pass

    @property
    @abstractmethod
    def _close(self):
        pass

    @_close.getter
    @abstractmethod
    def close(self) -> ArrayLike:
        pass

    @property
    @abstractmethod
    def _vol(self):
        pass

    @_vol.getter
    @abstractmethod
    def vol(self) -> ArrayLike:
        pass

    @property
    @abstractmethod
    def _time(self):
        pass

    @_time.getter
    @abstractmethod
    def time(self) -> ArrayLike:
        pass


class DefaultPriceSequence(PriceSequence):
    def __init__(self, price_seq: ArrayLike):
        """
        :param price_seq: 2d-array-like object
            Column of Open, High, Low, Close, Vol and Time must be arranged
            in this order.
            Rows must be ordered from latest bar to the oldest bar.
        """
        self.price_seq = price_seq

    @property
    def _open(self):
        pass

    @_open.getter
    def open(self) -> ArrayLike:
        return self.price_seq[:, 0]

    @property
    def _high(self):
        pass

    @_high.getter
    def high(self) -> ArrayLike:
        return self.price_seq[:, 1]

    @property
    def _low(self):
        pass

    @_low.getter
    def low(self) -> ArrayLike:
        return self.price_seq[:, 2]

    @property
    def _close(self):
        pass

    @_close.getter
    def close(self) -> ArrayLike:
        return self.price_seq[:, 3]

    @property
    def _vol(self):
        pass

    @_vol.getter
    def vol(self) -> ArrayLike:
        return self.price_seq[:, 4]

    @property
    def _time(self):
        pass

    @_time.getter
    def time(self) -> ArrayLike:
        return self.price_seq[:, 5]


class Bar(NamedTuple):
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    vol: int
    time: int
