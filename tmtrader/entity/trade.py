from decimal import Decimal
from typing import NamedTuple


class Entry(NamedTuple):
    timestamp: float
    price: Decimal


class Exit(NamedTuple):
    timestamp: float
    price: Decimal


class Trade(NamedTuple):
    product_id: int
    n_shares: int
    is_long: bool
    entry: Entry
    exit: Exit
    pl: Decimal
