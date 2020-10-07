from logging import getLogger

from tmtrader.controller.position_data_controller import PositionDataController
from tmtrader.entity.price import PriceSequence
from tmtrader.usecase.price_feed import PriceObserver
from tmtrader.usecase.send_order import OrderSender
from tmtrader.usecase.strategy import BaseStrategy, Strategy

logger = getLogger(__name__)


class StrategyProcessor(PriceObserver, OrderSender):
    def __init__(self, position_data: PositionDataController):
        super().__init__()
        self.__strategies = list()
        self.__position_data = position_data

    def add(self, strategy: Strategy):
        self.__strategies.append(strategy)

    def remove(self, strategy: Strategy):
        self.__strategies.remove(strategy)

    def notify_price_update(self, price_ref: PriceSequence):
        self.__run(price_ref)

    def __run(self, price_ref: PriceSequence):
        logger.debug(f'open: {price_ref.open[0]}, high: {price_ref.high[0]}, '
                     f'low: {price_ref.low[0]}, '
                     f'close: {price_ref.close[0]}, time: {price_ref.time[0]}')
        base = BaseStrategy(price_ref, self.__position_data.get_ref())
        may_orders = [base.execute(s) for s in self.__strategies]
        # may_ordersは空リストかもしれないし、各要素がNoneかもしれない
        orders = [o for o in may_orders if o]
        self._notify_new_orders(orders)
