from abc import abstractmethod
from decimal import Decimal
from logging import getLogger
from typing import List

from tmtrader.entity.order import BasicOrder, BuyLimitOrder, BuyMarketOrder, \
    BuyOrder, BuyStopOrder, SellLimitOrder, \
    SellMarketOrder, SellOrder, SellStopOrder
from tmtrader.exchange_for_backtest.usecase.order_spec import OrderSpec
from tmtrader.usecase.send_order import OrderObserver, OrderSender

logger = getLogger(__name__)


class OrderClient(OrderSender):
    @abstractmethod
    def buy_limit(self, product_id: int, price: Decimal, n_shares: int,
                  nth_bar: int):
        pass

    @abstractmethod
    def buy_market(self, product_id: int, n_shares: int, nth_bar: int):
        pass

    @abstractmethod
    def buy_stop(self, product_id: int, price: Decimal, n_shares: int,
                 nth_bar: int):
        pass

    @abstractmethod
    def sell_limit(self, product_id: int, price: Decimal, n_shares: int,
                   nth_bar: int):
        pass

    @abstractmethod
    def sell_market(self, product_id: int, n_shares: int, nth_bar: int):
        pass

    @abstractmethod
    def sell_stop(self, product_id: int, price: Decimal, n_shares: int,
                  nth_bar: int):
        pass


class OrderController(OrderObserver):
    pass


class DefaultOrderController(OrderController):
    def __init__(self, order_client: OrderClient, order_spec: OrderSpec):
        self.__order_client = order_client
        self.__order_spec = order_spec

    def notify_new_orders(self, orders: List[BasicOrder]):
        allowed_orders = self.__order_spec.filter(orders)
        self._handle_orders(allowed_orders)

    def _handle_orders(self, orders: List[BasicOrder]):
        [self._handle_order(o) for o in orders]

    def _handle_order(self, order: BasicOrder):
        if isinstance(order, BuyOrder):
            self._buy(order)
        elif isinstance(order, SellOrder):
            self._sell(order)
        else:
            raise RuntimeError(
                f'Got unexpected order type `{type(order)}`: {order}')

    def _buy(self, order: BuyOrder):
        if isinstance(order, BuyLimitOrder):
            self.__order_client.buy_limit(order.product_id, order.price,
                                          order.n_shares, order.nth_bar)
        elif isinstance(order, BuyMarketOrder):
            self.__order_client.buy_market(order.product_id, order.n_shares,
                                           order.nth_bar)
        elif isinstance(order, BuyStopOrder):
            self.__order_client.buy_stop(order.product_id, order.price,
                                         order.n_shares, order.nth_bar)

    def _sell(self, order: SellOrder):
        if isinstance(order, SellLimitOrder):
            self.__order_client.sell_limit(order.product_id, order.price,
                                           order.n_shares, order.nth_bar)
        elif isinstance(order, SellMarketOrder):
            self.__order_client.sell_market(order.product_id, order.n_shares,
                                            order.nth_bar)
        elif isinstance(order, SellStopOrder):
            self.__order_client.sell_stop(order.product_id, order.price,
                                          order.n_shares, order.nth_bar)
