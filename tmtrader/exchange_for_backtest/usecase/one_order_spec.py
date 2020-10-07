from logging import getLogger
from typing import List

from tmtrader.controller.order_history_controller import OrderHistoryController
from tmtrader.entity.order import BasicOrder, BuyOrder, SellOrder, \
    buy_sell_split
from tmtrader.exchange_for_backtest.usecase.order_spec import OrderSpec

logger = getLogger(__name__)


class OneOrderSpec(OrderSpec):
    def __init__(self, order_history_ref: OrderHistoryController):
        self.__order_history_ctr = order_history_ref

    def filter(self, orders: List[BasicOrder]):
        # TODO: Implement specification class that filter orders to be sent
        #  to OrderController.
        #   - Only one order can be sent at a time for each buy and sell.
        #   - No new order that will have new positions can be sent when the
        #     trader already has one or more positions.
        #   - sending new order is not allowed when there is already an open
        #     order of same side.
        allowed_orders = self.__no_new_order_when_exists_open_order(orders)
        allowed_orders = self.__only_one_order_for_each_side(allowed_orders)

        return allowed_orders

    def __no_new_order_when_exists_open_order(self, orders):
        buy_orders, sell_orders = buy_sell_split(orders)

        open_orders = self.__order_history_ctr.list_open_orders()
        if [o for o in open_orders if isinstance(o, BuyOrder)]:
            buy_orders = []

        if [o for o in open_orders if isinstance(o, SellOrder)]:
            sell_orders = []

        return buy_orders + sell_orders

    def __only_one_order_for_each_side(self, orders):
        allowed_orders: List[BasicOrder] = []
        buy_orders, sell_orders = buy_sell_split(orders)

        if buy_orders:
            allowed_orders.append(buy_orders[0])

        if sell_orders:
            allowed_orders.append(sell_orders[0])

        return allowed_orders
