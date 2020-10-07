from logging import getLogger
from typing import Optional

from tmtrader.entity.order import Order, SellMarketOrder
from tmtrader.entity.position import PositionsRefForClient
from tmtrader.entity.price import PriceSequence
from tmtrader.usecase.strategy import Strategy

logger = getLogger(__name__)

class ExitSellWithTargetProfit(Strategy):
    def __init__(self, target_profit: float):
        self.__target_profit = target_profit

    def execute(self,
                d: PriceSequence,
                p: PositionsRefForClient) -> Optional[Order]:
        if p.has_positions():
            current_profit = d.close[0] - float(p.position.filled_price)
            if current_profit >= self.__target_profit:
                logger.debug('sell market')
                return SellMarketOrder(d.time[0], 0, 1, 1)
