from logging import getLogger
from typing import List

from tmtrader.entity.order import FilledBasicOrder, Order
from tmtrader.entity.trade import Trade
from tmtrader.exchange_for_backtest.order_manager import OrderManager
from tmtrader.exchange_for_backtest.position_manager import PositionManager
from tmtrader.exchange_for_backtest.usecase.close_order import \
    OrderCloseObserver
from tmtrader.exchange_for_backtest.usecase.position_to_trade import \
    from_closed_position

logger = getLogger(__name__)


class AccountManager:
    pass


class TradeManager(OrderCloseObserver):
    def __init__(self, position_mng: PositionManager,
                 order_mng: OrderManager,
                 account_mng: AccountManager = None):
        self.__position_mng = position_mng
        self.__order_mng = order_mng
        self.__account_mng = account_mng

    @property
    def trade_history(self) -> List[Trade]:
        return self.__order_mng.trades

    def notify_order_filled(self, order: FilledBasicOrder):
        # self.__position_mng.update_position(order)
        closed_positions = self.__position_mng.update_position(order)
        # logger.debug(closed_positions)
        self.__order_mng.add_filled_orders([order])
        self.__order_mng.add_trades(
            [from_closed_position(p) for p in closed_positions])
        # self.__order_mng.add_filled_order(order)
        # self.__account_mng.update_balance(order)

    def notify_order_cancelled(self, order: Order):
        logger.warning('not implemented yet.')
        pass
