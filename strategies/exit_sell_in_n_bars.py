from logging import getLogger
from typing import Optional

from tmtrader.entity.order import Order, SellMarketOrder
from tmtrader.entity.position import PositionsRefForClient
from tmtrader.entity.price import PriceSequence
from tmtrader.usecase.strategy import Strategy

logger = getLogger(__name__)

N_BARS = 5


class ExitSellInNBars(Strategy):
    def __init__(self, n_bars: Optional[int] = None):
        self.__n_bars = n_bars if n_bars else N_BARS

    def execute(self,
                d: PriceSequence,
                p: PositionsRefForClient) -> Optional[Order]:
        if p.has_positions() \
                and p.longest_holding_period_bars(d.time[0]) >= self.__n_bars:
            logger.debug('sell market')
            return SellMarketOrder(d.time[0], 0, 1, 1)
