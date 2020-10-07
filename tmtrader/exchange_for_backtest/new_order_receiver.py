from typing import List

from tmtrader.entity.order import BasicOrder
from tmtrader.usecase.send_order import OrderObserver, OrderSender


class NewOrderReceiver(OrderSender, OrderObserver):
    def __init__(self):
        super().__init__()

    def notify_new_orders(self, orders: List[BasicOrder]):
        self._notify_new_orders(orders)

