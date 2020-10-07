from decimal import Decimal
from logging import getLogger
from typing import List, NamedTuple, Optional

from tmtrader.entity.order import BasicOrder, BuyLimitOrder, BuyMarketOrder, \
    BuyStopOrder, FilledBasicOrder, FilledBuyLimitOrder, \
    FilledBuyMarketOrder, \
    FilledBuyStopOrder, FilledSellLimitOrder, FilledSellMarketOrder, \
    FilledSellStopOrder, OrderCondition, OrderStatus, OrderType, \
    SellLimitOrder, SellMarketOrder, SellStopOrder
from tmtrader.entity.price import Bar
from tmtrader.exchange_for_backtest.price_stream import PriceStream
from tmtrader.exchange_for_backtest.usecase.close_order import \
    OrderCloseNotifier
from tmtrader.usecase.send_order import OrderObserver
from tmtrader.usecase.time_ref import DefaultTimeRef, TimeRef

logger = getLogger(__name__)


class Filled(NamedTuple):
    price: Decimal
    n_shares: int


class BackTestBroker(OrderObserver, OrderCloseNotifier):
    def __init__(self, price_stream_ref: PriceStream,
                 time_ref: Optional[TimeRef] = None):
        super().__init__()
        self.__price_stream_ref = price_stream_ref
        self.__open_orders: List[BasicOrder] = list()
        if time_ref is None:
            time_ref = DefaultTimeRef()
        self.__time_ref = time_ref

    def notify_new_orders(self, orders: List[BasicOrder]):
        self.__place_orders(orders)

    def __place_orders(self, orders: List[BasicOrder]):
        self.__open_orders.extend(orders)
        self.__try_fill_with_latest_price()

    def __try_fill_with_latest_price(self):
        bar = self.__price_stream_ref.get_latest_bar_decimal()
        may_filled_orders = [_try_fill(o, bar) for o in self.__open_orders]
        fos = [self._notify_order_filled(o) for o in may_filled_orders if
               o is not None]
        self.__open_orders = [o for o in self.__open_orders if
                              o.status == OrderStatus.OPEN]
        # logger.debug(
        #     f'len(filled orders) = {len(fos)}, len(open orders) '
        #     f'= {len(self.__orders)}')


def _try_fill(order: BasicOrder, bar: Bar) -> Optional[FilledBasicOrder]:
    filled_order = None
    if isinstance(order, BuyLimitOrder):
        filled = _buy_limit(order.price, order.n_shares, bar)
        if filled:
            filled_order = FilledBuyLimitOrder.from_order(order,
                                                          filled.price,
                                                          filled.n_shares,
                                                          bar.time)
    elif isinstance(order, BuyMarketOrder):
        filled = _buy_market(order.n_shares, bar)
        if filled:
            filled_order = FilledBuyMarketOrder.from_order(order,
                                                           filled.price,
                                                           filled.n_shares,
                                                           bar.time)
    elif isinstance(order, BuyStopOrder):
        filled = _buy_stop(order.price, order.n_shares, bar)
        if filled:
            filled_order = FilledBuyStopOrder.from_order(order,
                                                         filled.price,
                                                         filled.n_shares,
                                                         bar.time)
    elif isinstance(order, SellLimitOrder):
        filled = _sell_limit(order.price, order.n_shares, bar)
        if filled:
            filled_order = FilledSellLimitOrder.from_order(order,
                                                           filled.price,
                                                           filled.n_shares,
                                                           bar.time)
    elif isinstance(order, SellMarketOrder):
        filled = _sell_market(order.n_shares, bar)
        if filled:
            filled_order = FilledSellMarketOrder.from_order(order,
                                                            filled.price,
                                                            filled.n_shares,
                                                            bar.time)
    elif isinstance(order, SellStopOrder):
        filled = _sell_stop(order.price, order.n_shares, bar)
        if filled:
            filled_order = FilledSellStopOrder.from_order(order,
                                                          filled.price,
                                                          filled.n_shares,
                                                          bar.time)
    else:
        TypeError(
            f'`order` must be an instance of BasicOrder, but got type `'
            f'{type(order)}`.')

    # TODO: これは単なるフラグだから書かなくても良くなるようにリファクタリングする
    if filled_order:
        order.filled()

    return filled_order


def _buy_limit(price: Decimal, n_shares: int, bar: Bar):
    if bar.low <= price <= bar.high:
        # logger.debug('BuyLimitOrder filled.')
        return Filled(price, n_shares)
    else:
        return None


def _buy_market(n_shares: int, bar: Bar):
    return Filled(bar.open, n_shares)


def _buy_stop(price: Decimal, n_shares: int, bar: Bar):
    if bar.low <= price <= bar.high:
        return Filled(price, n_shares)
    else:
        return None


def _sell_limit(price: Decimal, n_shares: int, bar: Bar):
    if bar.low <= price <= bar.high:
        return Filled(price, n_shares)
    else:
        return None


def _sell_market(n_shares: int, bar: Bar):
    # logger.debug('SellMarketOrder filled.')
    return Filled(bar.open, n_shares)


def _sell_stop(price: Decimal, n_shares: int, bar: Bar):
    if bar.low <= price <= bar.high:
        return Filled(price, n_shares)
    else:
        return None


# TODO: delete if unnecessary
def _create_open_order(timestamp: float, product_id: int, n_shares: int,
                       nth_bar: int, type_: OrderType,
                       condition: OrderCondition,
                       price: Optional[Decimal] = None) -> BasicOrder:
    if type_ == OrderType.BUY:
        if condition == OrderCondition.LIMIT:
            return BuyLimitOrder(timestamp, product_id, n_shares, price,
                                 nth_bar, OrderStatus.OPEN)
        elif condition == OrderCondition.MARKET:
            return BuyMarketOrder(timestamp, product_id, n_shares, nth_bar,
                                  OrderStatus.OPEN)
        elif condition == OrderCondition.STOP:
            return BuyStopOrder(timestamp, product_id, n_shares, price,
                                nth_bar, OrderStatus.OPEN)
        else:
            raise ValueError(
                f'condition must be one of LIMIT, MARKET and STOP, but got '
                f'`{condition}`.')
    elif type_ == OrderType.SELL:
        if condition == OrderCondition.LIMIT:
            return SellLimitOrder(timestamp, product_id, n_shares, price,
                                  nth_bar, OrderStatus.OPEN)
        elif condition == OrderCondition.MARKET:
            return SellMarketOrder(timestamp, product_id, n_shares, nth_bar,
                                   OrderStatus.OPEN)
        elif condition == OrderCondition.STOP:
            return SellStopOrder(timestamp, product_id, n_shares, price,
                                 nth_bar, OrderStatus.OPEN)
        else:
            raise ValueError(
                f'condition must be one of LIMIT, MARKET and STOP, but got '
                f'`{condition}`.')
    else:
        raise ValueError(f'type_ must be BUY or SELL, but got `{type_}`.')
