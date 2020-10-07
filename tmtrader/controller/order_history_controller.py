from abc import ABC, abstractmethod
from typing import List

from tmtrader.entity.order import BasicOrder
from tmtrader.entity.trade import Trade


class OrderManagerClient(ABC):
    @abstractmethod
    def list_open_orders(self) -> List[BasicOrder]:
        pass

    @abstractmethod
    def list_trade_history(self) -> List[Trade]:
        pass

    @abstractmethod
    def list_filled_orders(self) -> List[BasicOrder]:
        pass

    @abstractmethod
    def list_cancelled_orders(self) -> List[BasicOrder]:
        pass


class OrderHistoryController(ABC):
    @abstractmethod
    def list_open_orders(self) -> List[BasicOrder]:
        pass


class BTOrderHistoryController(OrderHistoryController):
    def __init__(self, order_mng_client: OrderManagerClient):
        self.__order_mng_client = order_mng_client

    def list_open_orders(self) -> List[BasicOrder]:
        return self.__order_mng_client.list_open_orders()
