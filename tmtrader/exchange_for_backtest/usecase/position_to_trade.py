from tmtrader.entity.position import ClosedPosition
from tmtrader.entity.trade import Entry, Exit, Trade


def from_closed_position(position: ClosedPosition):
    pl = position.exit.filled_price - position.entry.filled_price
    if not position.is_long:
        pl = -pl

    return Trade(
        position.entry.product_id, 1, position.is_long,
        Entry(position.entry.filled_time, position.entry.filled_price),
        Exit(position.exit.filled_time, position.exit.filled_price),
        pl
    )
