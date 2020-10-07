from abc import ABC, abstractmethod
from typing import Optional

from tmtrader.controller.position_data_controller import PositionDataRef
from tmtrader.entity.order import Order
from tmtrader.entity.position import PositionsRefForClient, empty_positions_ref
from tmtrader.entity.price import PriceSequence

# TODO: set this value at strategy settings
PRODUCT1 = 0


class Strategy(ABC):
    @abstractmethod
    def execute(self,
                d: PriceSequence,
                p: PositionsRefForClient) -> Optional[Order]:
        pass


class BaseStrategy:
    def __init__(self,
                 d: PriceSequence,
                 p: PositionDataRef):
        self.__d = d
        self.__p = p

    def execute(self, s: Strategy) -> Optional[Order]:
        if PRODUCT1 in self.__p.positions:
            positions = self.__p.positions[PRODUCT1]
        else:
            positions = empty_positions_ref(PRODUCT1)

        return s.execute(self.__d, positions)
