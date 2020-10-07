from logging import getLogger
from typing import Dict, List, Optional

from tmtrader.entity.order import FilledBasicOrder
from tmtrader.entity.position import ClosedPosition, Position, Positions, \
    PositionsRef
from tmtrader.exchange_for_backtest.usecase.order_to_share import from_order

logger = getLogger(__name__)

PositionsDict = Dict[int, Positions]
ClosedPositions = List[ClosedPosition]


class PositionManager:
    def __init__(self):
        self.__positions_dic: PositionsDict = dict()

    def current_positions_of(self, product_id: int) -> Optional[PositionsRef]:
        if product_id in self.__positions_dic:
            return self.__positions_dic[product_id].to_ref()
        else:
            return None

    def current_positions(self) -> Dict[int, PositionsRef]:
        return {k: v.to_ref() for k, v in self.__positions_dic.items() if
                v.len}

    def update_position(self,
                        order: FilledBasicOrder) -> ClosedPositions:
        logger.debug(f'Got filled order at PositionManager: {order}')
        pid = order.product_id
        if pid in self.__positions_dic:
            logger.debug(f'position size before update: {self.__positions_dic[pid].len}')
        else:
            logger.debug(f'position size before update: 0')
        new_shares = from_order(order)

        positions = None
        if pid in self.__positions_dic:
            positions = self.__positions_dic.pop(pid)

        closed_pos = []
        if positions and positions.is_long:
            if order.is_buy:
                self.__add_positions(pid, positions, new_shares)
            else:
                closed_pos = self.__close_and_may_open(pid, positions,
                                                       new_shares)
        elif positions:
            if order.is_buy:
                closed_pos = self.__close_and_may_open(pid, positions,
                                                       new_shares)
            else:
                self.__add_positions(pid, positions, new_shares)
        else:
            self.__positions_dic[pid] = Positions(pid, new_shares,
                                                  order.is_buy)

        if pid in self.__positions_dic:
            logger.debug(
                f'position size after update: {self.__positions_dic[pid].len}')
        else:
            logger.debug('position size after update: 0')

        return closed_pos

    def __add_positions(self, pid: int, positions: Positions,
                        new_shares: List[Position]):
        positions.add_positions(new_shares)
        self.__positions_dic[pid] = positions

    def __close_and_may_open(self, pid: int, positions: Positions,
                             new_shares: List[Position]) -> ClosedPositions:
        closed = positions.close_positions(new_shares)
        if closed.remaining_contracts:
            self.__positions_dic[pid] = Positions(pid,
                                                  closed.remaining_contracts,
                                                  is_long=not
                                                  positions.is_long)
        else:
            if positions.len:
                self.__positions_dic[pid] = positions

        return closed.closed
