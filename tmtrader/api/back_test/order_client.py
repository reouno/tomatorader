from decimal import Decimal
from logging import getLogger
from typing import List, Optional

from tmtrader.controller.order_controller import OrderClient
from tmtrader.entity.order import BasicOrder, OrderType, OrderCondition, \
    BuyLimitOrder, BuyMarketOrder, BuyStopOrder, \
    SellLimitOrder, SellMarketOrder, SellStopOrder, OrderStatus
from tmtrader.exchange_for_backtest.back_test_broker import BackTestBroker
from tmtrader.usecase.send_order import OrderSender
from tmtrader.usecase.time_ref import TimeRef, DefaultTimeRef

logger = getLogger(__name__)


class BackTestOrderClient(OrderClient):
    def __init__(self, time_ref: Optional[TimeRef] = None):
        super().__init__()
        self.orders: List[BasicOrder] = list()
        if time_ref is None:
            time_ref = DefaultTimeRef()
        self.__time_ref = time_ref

    def buy_limit(self, product_id: int, price: Decimal, n_shares: int,
                  nth_bar: int):
        if price is None:
            raise AttributeError(f'`price` must not be None in limit order.')
        self._notify_new_orders(
            [BuyLimitOrder(self.__time_ref.now(), product_id, n_shares, price,
                           nth_bar)])
        # logger.debug(
        #     f'called buy_limit with product_id:{product_id}, price:{price}, '
        #     f'n_shares:{n_shares}')

    def buy_market(self, product_id: int, n_shares: int, nth_bar: int):
        self._notify_new_orders(
            [BuyMarketOrder(self.__time_ref.now(), product_id, n_shares,
                            nth_bar)])
        # logger.debug(
        #     f'called buy_market with product_id:{product_id}, n_shares:'
        #     f'{n_shares}')

    def buy_stop(self, product_id: int, price: Decimal, n_shares: int,
                 nth_bar: int):
        if price is None:
            raise AttributeError(f'`price` must not be None in stop order.')
        self._notify_new_orders(
            [BuyStopOrder(self.__time_ref.now(), product_id, n_shares, price,
                          nth_bar)])
        # logger.debug(
        #     f'called buy_stop with product_id:{product_id}, price:{price}, '
        #     f'n_shares:{n_shares}')

    def sell_limit(self, product_id: int, price: Decimal, n_shares: int,
                   nth_bar: int):
        if price is None:
            raise AttributeError(f'`price` must not be None in limit order.')
        self._notify_new_orders(
            [SellLimitOrder(self.__time_ref.now(), product_id, n_shares, price,
                            nth_bar)])
        # logger.debug(
        #     f'called sell_limit with product_id:{product_id}, price:{price}, '
        #     f'n_shares:{n_shares}')

    def sell_market(self, product_id: int, n_shares: int, nth_bar: int):
        self._notify_new_orders(
            [SellMarketOrder(self.__time_ref.now(), product_id, n_shares,
                             nth_bar)])
        # logger.debug(
        #     f'called sell_market with product_id:{product_id}, n_shares:'
        #     f'{n_shares}')

    def sell_stop(self, product_id: int, price: Decimal, n_shares: int,
                  nth_bar: int):
        if price is None:
            raise AttributeError(f'`price` must not be None in stop order.')
        self._notify_new_orders(
            [SellStopOrder(self.__time_ref.now(), product_id, n_shares, price,
                           nth_bar)])
        # logger.debug(
        #     f'called sell_stop with product_id:{product_id}, price:{price}, n_shares:{n_shares}')
