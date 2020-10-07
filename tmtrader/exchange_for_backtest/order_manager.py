from typing import List

from tmtrader.entity.order import BasicOrder, FilledBasicOrder
from tmtrader.entity.trade import Trade


class OrderManager:
    def __init__(self):
        self.__open_orders: List[BasicOrder] = list()
        self.__filled_orders: List[FilledBasicOrder] = list()

        # TODO: refactor and define ClosedOrder and CancelledOrder
        self.__cancelled_orders: List[BasicOrder] = list()
        self.__trades: List[Trade] = list()

    @property
    def open_orders(self) -> List[BasicOrder]:
        return self.__open_orders

    @property
    def filled_orders(self) -> List[FilledBasicOrder]:
        return self.__filled_orders

    @property
    def cancelled_orders(self) -> List[BasicOrder]:
        return self.__cancelled_orders

    @property
    def trades(self) -> List[Trade]:
        return self.__trades

    def add_open_orders(self, orders: List[BasicOrder]):
        self.__open_orders.extend(orders)

    def add_filled_orders(self, orders: List[FilledBasicOrder]):
        self.__filled_orders.extend(orders)

    def add_cancelled_orders(self, orders: List[BasicOrder]):
        self.__cancelled_orders.extend(orders)

    def add_trades(self, trades: List[Trade]):
        self.__trades.extend(trades)
