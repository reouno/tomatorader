from logging import getLogger
from typing import Dict, Optional

from tmtrader.entity.position import PositionsRef
from tmtrader.exchange_for_backtest.position_manager import PositionManager

logger = getLogger(__name__)


class PositionClient:
    def __init__(self, position_mng: PositionManager):
        self.__position_mng = position_mng

    def get(self, product_id: int) -> Optional[PositionsRef]:
        return self.__position_mng.current_positions_of(product_id)

    def list(self) -> Dict[int, PositionsRef]:
        return self.__position_mng.current_positions()
