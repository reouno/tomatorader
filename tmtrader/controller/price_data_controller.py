from abc import ABC

from tmtrader.entity.price import PriceSequence
from tmtrader.usecase.price_feed import PriceFeeder, PriceObserver


class PriceDataController(PriceFeeder, PriceObserver):
    pass


class BTPriceDataController(PriceDataController):
    def notify_price_update(self, price_ref: PriceSequence):
        self._notify_price_update(price_ref)
