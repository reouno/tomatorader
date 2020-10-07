from abc import abstractmethod

from tmtrader.entity.price import PriceSequence, Bar
from tmtrader.usecase.price_feed import PriceFeeder


class PriceStream(PriceFeeder):
    @abstractmethod
    def start_feed(self):
        pass

    @abstractmethod
    def get_latest_bars(self, n_bars: int = 1) -> PriceSequence:
        pass

    @abstractmethod
    def get_latest_bar_decimal(self) -> Bar:
        pass
