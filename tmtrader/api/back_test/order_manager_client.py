from typing import List

from tmtrader.controller.order_history_controller import OrderManagerClient
from tmtrader.entity.order import BasicOrder
from tmtrader.entity.trade import Trade
from tmtrader.exchange_for_backtest.order_manager import OrderManager


class BTOrderManagerClient(OrderManagerClient):
    def __init__(self, order_mng: OrderManager):
        self.__order_mng = order_mng

    def list_open_orders(self) -> List[BasicOrder]:
        return self.__order_mng.open_orders

    def list_trade_history(self) -> List[Trade]:
        return self.__order_mng.trades

    def list_filled_orders(self) -> List[BasicOrder]:
        return self.__order_mng.filled_orders

    def list_cancelled_orders(self) -> List[BasicOrder]:
        return self.__order_mng.cancelled_orders