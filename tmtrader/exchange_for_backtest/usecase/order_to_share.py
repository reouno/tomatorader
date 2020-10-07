from typing import List

from tmtrader.entity.order import FilledBasicOrder
from tmtrader.entity.position import Position


def from_order(order: FilledBasicOrder) -> List[Position]:
    share = Position(order.product_id, order.filled_time,
                     order.filled_price, order.is_buy)
    return [share] * order.filled_n_shares
