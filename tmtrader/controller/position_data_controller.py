from abc import ABC, abstractmethod
from typing import Dict, Optional, NamedTuple

from tmtrader.api.back_test.position_client import PositionClient
from tmtrader.entity.position import PositionsRef, PositionsRefForClient, \
    create_positions_ref


class PositionDataRef(NamedTuple):
    positions: Dict[int, PositionsRefForClient]


class PositionDataController(ABC):
    @abstractmethod
    def get_ref(self) -> PositionDataRef:
        pass


class BTPositionDataController(PositionDataController):
    def __init__(self, position_client: PositionClient):
        self.__position_client = position_client

    def get_ref(self) -> PositionDataRef:
        return PositionDataRef({k: create_positions_ref(v) for k, v in
                                self.__get_current_positions().items()})

    def __get_current_positions(self) -> Dict[int, PositionsRef]:
        return self.__position_client.list()

    def __get_current_positions_of(self,
                                   product_id: int) -> Optional[PositionsRef]:
        return self.__position_client.get(product_id)
