from logging import getLogger
from typing import Optional

import numpy as np

from tmtrader.entity.order import BuyMarketOrder, Order
from tmtrader.entity.position import PositionsRefForClient
from tmtrader.entity.price import PriceSequence
from tmtrader.usecase.strategy import Strategy

logger = getLogger(__name__)


class EntryBuyRandom(Strategy):
    def __init__(self, prob: float = 0.5):
        self.__prob = prob

    def execute(self,
                d: PriceSequence,
                p: PositionsRefForClient) -> Optional[Order]:
        v = np.random.rand()

        if p.has_positions():
            logger.debug(
                f'holding period bars of the current position: '
                f'{p.longest_holding_period_bars(d.time[0])}')

        if v <= self.__prob and not p.has_positions():
            logger.debug('buy limit')
            return BuyMarketOrder(d.time[0], 0, 1, 1)
