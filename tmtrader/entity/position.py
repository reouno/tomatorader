from collections import deque
from decimal import Decimal
from typing import List, NamedTuple, Optional


class Position(NamedTuple):
    product_id: int
    filled_time: float
    filled_price: Decimal
    is_buy: bool


class ClosedPosition(NamedTuple):
    entry: Position
    exit: Position
    is_long: bool


class ClosedResult(NamedTuple):
    closed: List[ClosedPosition]
    remaining_contracts: List[Position]


class PositionsRef(NamedTuple):
    product_id: int
    positions: List[Position]
    is_long: bool


class Positions:
    def __init__(self, product_id: int, positions: List[Position],
                 is_long: bool):
        self.__product_id = product_id
        self.__positions = deque(positions)
        self.__is_long = is_long

    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def is_long(self) -> bool:
        return self.__is_long

    @property
    def len(self) -> int:
        return len(self.__positions)

    def add_positions(self, contracts: List[Position]):
        if contracts and contracts[0].is_buy != self.__is_long:
            raise ValueError(f'cannot add the opposite side positions, '
                             f'current is_long={self.__is_long}, '
                             f'new is_buy={contracts[0].is_buy}.')

        self.__positions.extend(contracts)

    def close_positions(self, contracts: List[Position]) -> ClosedResult:
        if contracts and contracts[0].is_buy == self.__is_long:
            raise ValueError(f'cannot close with the same side positions, '
                             f'current is_long={self.__is_long}, '
                             f'new is_buy={contracts[0].is_buy}.')

        if len(self.__positions) >= len(contracts):
            closed = [
                ClosedPosition(self.__positions.popleft(), contracts[i],
                               is_long=self.__is_long)
                for i in range(len(contracts))]
            return ClosedResult(closed, [])
        else:
            closed_opp = contracts[:len(self.__positions)]
            remaining = contracts[len(self.__positions):]
            return ClosedResult(
                [ClosedPosition(self.__positions.popleft(), o, self.__is_long)
                 for
                 o in closed_opp], remaining)

    def to_ref(self) -> PositionsRef:
        return PositionsRef(self.__product_id, list(self.__positions),
                            self.__is_long)


class PositionsRefForClient:
    def __init__(self, product_id: int, positions: List[Position],
                 is_long: bool):
        self.__product_id = product_id
        self.__positions = positions
        self.__is_long = is_long

    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def positions(self) -> List[Position]:
        return self.__positions

    @property
    def is_long(self) -> bool:
        return self.__is_long

    @property
    def size(self) -> int:
        return len(self.__positions)

    @property
    def position(self) -> Optional[Position]:
        # The first (left end) position is always the oldest one.
        if self.has_positions():
            return self.__positions[0]
        else:
            return None

    def has_positions(self) -> bool:
        return self.size > 0

    # FIXME: define time (= bar count) and timestamp (= unix time) each
    #        time is int and timestamp is float
    def longest_holding_period_bars(self, current: int) -> int:
        if self.has_positions():
            return round(current - self.position.filled_time)
        else:
            return 0



def create_positions_ref(ref: PositionsRef) -> PositionsRefForClient:
    return PositionsRefForClient(ref.product_id, ref.positions, ref.is_long)


def empty_positions_ref(product_id: int) -> PositionsRefForClient:
    return PositionsRefForClient(product_id, [], False)
