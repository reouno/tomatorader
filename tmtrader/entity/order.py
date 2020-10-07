from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum, auto
from typing import List, NamedTuple


class OrderType(Enum):
    BUY = auto()
    SELL = auto()


class OrderCondition(Enum):
    LIMIT = auto()
    MARKET = auto()
    STOP = auto()


class OrderStatus(Enum):
    OPEN = auto()
    FILLED = auto()
    CANCELLED = auto()


class Bar(Enum):
    THIS = 0
    NEXT = 1


# TODO: deleted if not necessary
class Order(ABC):
    @property
    @abstractmethod
    def is_buy(self) -> bool:
        pass


class BasicOrder(Order):
    def __init__(self, time_: float, product_id: int, n_shares: int,
                 nth_bar: int):
        self.__time = time_
        self.__product_id = product_id
        self.__n_shares = n_shares
        self.__nth_bar = nth_bar
        self.__status = OrderStatus.OPEN
        self.__validate_inputs()

    @property
    def time(self) -> float:
        return self.__time

    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def n_shares(self) -> int:
        return self.__n_shares

    @property
    def nth_bar(self) -> int:
        return self.__nth_bar

    @property
    def status(self) -> OrderStatus:
        return self.__status

    @property
    @abstractmethod
    def is_buy(self) -> bool:
        pass

    def decrement_nth_bar(self):
        if self.__nth_bar > 0:
            self.__nth_bar -= 1

    def filled(self):
        self.__status = OrderStatus.FILLED

    def cancelled(self):
        self.__status = OrderStatus.CANCELLED

    def __validate_inputs(self) -> None:
        if self.__n_shares < 1:
            raise AttributeError(
                f'`n_shares` must be an int greater than or equal to 1, '
                f'but got `{self.__n_shares}`.')
        if self.__nth_bar < 0:
            raise AttributeError(
                f'`nth_bar` must be and int greater than or equal to 0, '
                f'but got `{self.__nth_bar}`.')


class WithPrice(ABC):
    @property
    @abstractmethod
    def price(self) -> Decimal:
        pass


class BasicOrderWithPrice(BasicOrder, WithPrice):
    def __init__(self, time_: float, product_id: int, n_shares: int,
                 price: Decimal, nth_bar: int):
        super().__init__(time_, product_id, n_shares, nth_bar)
        self.__price = price
        self.__validate_inputs()

    @property
    def price(self) -> Decimal:
        return self.__price

    @property
    @abstractmethod
    def is_buy(self) -> bool:
        pass

    def __validate_inputs(self) -> None:
        if self.__price <= 0:
            raise AttributeError(
                f'`price` must be Decimal greater than 0, but got `'
                f'{self.__price}`.')


class BuyOrder:
    pass


class SellOrder:
    pass


class BuyLimitOrder(BasicOrderWithPrice, BuyOrder):
    @property
    def is_buy(self) -> bool:
        return True


class BuyMarketOrder(BasicOrder, BuyOrder):
    @property
    def is_buy(self) -> bool:
        return True


class BuyStopOrder(BasicOrderWithPrice, BuyOrder):
    @property
    def is_buy(self) -> bool:
        return True


class SellLimitOrder(BasicOrderWithPrice, SellOrder):
    @property
    def is_buy(self) -> bool:
        return False


class SellMarketOrder(BasicOrder, SellOrder):
    @property
    def is_buy(self) -> bool:
        return False


class SellStopOrder(BasicOrderWithPrice, SellOrder):
    @property
    def is_buy(self) -> bool:
        return False


class FilledOrder(ABC):
    @property
    @abstractmethod
    def filled_price(self) -> Decimal:
        pass

    @property
    @abstractmethod
    def filled_n_shares(self) -> int:
        pass

    @property
    @abstractmethod
    def filled_time(self) -> float:
        pass

    @property
    @abstractmethod
    def is_buy(self) -> bool:
        pass


class FilledBasicOrder(BasicOrder, FilledOrder):
    @classmethod
    def from_order(cls, order: BasicOrder, filled_price: Decimal,
                   filled_n_shares: int, filled_time: float):
        return cls(order.time, order.product_id, order.n_shares,
                   order.nth_bar, filled_price, filled_n_shares,
                   filled_time)

    def __init__(self, time_: float, product_id: int, n_shares: int,
                 nth_bar: int, filled_price: Decimal,
                 filled_n_shares: int, filled_time: float):
        super().__init__(time_, product_id, n_shares, nth_bar)
        self.filled()
        self.__filled_price = filled_price
        self.__filled_n_shares = filled_n_shares
        self.__filled_time = filled_time

    @property
    def filled_price(self) -> Decimal:
        return self.__filled_price

    @property
    def filled_n_shares(self) -> int:
        return self.__filled_n_shares

    @property
    def filled_time(self) -> float:
        return self.__filled_time

    @property
    @abstractmethod
    def is_buy(self) -> bool:
        pass


class FilledBasicOrderWithPrice(FilledBasicOrder, WithPrice):
    @classmethod
    def from_order(cls, order: BasicOrderWithPrice,
                   filled_price: Decimal, filled_n_shares: int,
                   filled_time: float):
        return cls(order.time, order.product_id, order.n_shares,
                   order.price, order.nth_bar, filled_price,
                   filled_n_shares, filled_time)

    def __init__(self, time_: float, product_id: int, n_shares: int,
                 price: Decimal, nth_bar: int, filled_price: Decimal,
                 filled_n_shares: int, filled_time: float):
        super().__init__(time_, product_id, n_shares, nth_bar,
                         filled_price, filled_n_shares, filled_time)
        self.__price = price
        self.__validate_inputs()

    @property
    def price(self) -> Decimal:
        return self.__price

    @property
    @abstractmethod
    def is_buy(self) -> bool:
        pass

    def __validate_inputs(self) -> None:
        if self.__price <= 0:
            raise AttributeError(
                f'`price` must be Decimal greater than 0, but got `'
                f'{self.__price}`.')


class FilledBuyLimitOrder(FilledBasicOrderWithPrice, BuyOrder):
    @property
    def is_buy(self) -> bool:
        return True


class FilledBuyMarketOrder(FilledBasicOrder, BuyOrder):
    @property
    def is_buy(self) -> bool:
        return True


class FilledBuyStopOrder(FilledBasicOrderWithPrice, BuyOrder):
    @property
    def is_buy(self) -> bool:
        return True


class FilledSellLimitOrder(FilledBasicOrderWithPrice, SellOrder):
    @property
    def is_buy(self) -> bool:
        return False


class FilledSellMarketOrder(FilledBasicOrder, SellOrder):
    @property
    def is_buy(self) -> bool:
        return False


class FilledSellStopOrder(FilledBasicOrderWithPrice, SellOrder):
    @property
    def is_buy(self) -> bool:
        return False


class BuySellSplitResult(NamedTuple):
    buys: List[BasicOrder]
    sells: List[BasicOrder]


def buy_sell_split(orders: List[BasicOrder]):
    buy_orders = [o for o in orders if o.is_buy]
    sell_orders = [o for o in orders if not o.is_buy]
    return BuySellSplitResult(buys=buy_orders, sells=sell_orders)
