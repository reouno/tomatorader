from decimal import Decimal
from logging import getLogger
from typing import Optional

import numpy as np

from tmtrader.entity.order import BuyLimitOrder, Order, SellMarketOrder, \
    BuyMarketOrder
from tmtrader.entity.position import PositionsRefForClient
from tmtrader.entity.price import PriceSequence
from tmtrader.usecase.strategy import Strategy

logger = getLogger(__name__)


class MonkeyStrategy(Strategy):
    def execute(self,
                d: PriceSequence,
                p: PositionsRefForClient) -> Optional[Order]:
        v = np.random.rand()

        if p.has_positions():
            logger.debug(
                f'holding period bars of the current position: '
                f'{p.longest_holding_period_bars(d.time[0])}')

        if v >= 0.5 and not p.has_positions():
            logger.debug('buy limit')
            return BuyMarketOrder(d.time[0], 0, 1, 1)

        if v <= 0.3 and p.has_positions():
            logger.debug('sell market')
            return SellMarketOrder(d.time[0], 0, 1, 1)