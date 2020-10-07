from decimal import Decimal
from functools import lru_cache
from typing import List, Optional, Union

from tmtrader.controller.account_data_controller import AccountDataController
from tmtrader.controller.order_controller import OrderClient, OrderController
from tmtrader.controller.order_history_controller import OrderHistoryController
from tmtrader.controller.position_data_controller import PositionDataController
from tmtrader.controller.price_data_controller import PriceDataController
from tmtrader.controller.strategy_processor import StrategyProcessor
from tmtrader.entity.trade import Trade
from tmtrader.exchange_for_backtest.back_test_broker import BackTestBroker
from tmtrader.exchange_for_backtest.new_order_receiver import NewOrderReceiver
from tmtrader.exchange_for_backtest.price_stream import PriceStream
from tmtrader.exchange_for_backtest.trade_manager import TradeManager
from tmtrader.usecase.strategy import Strategy


class BTClient:
    def __init__(self,
                 price_data_controller: PriceDataController,
                 strategy_proc: StrategyProcessor,
                 order_controller: OrderController,
                 position_data_controller: PositionDataController,
                 order_history: OrderHistoryController,
                 account_data: AccountDataController,
                 order_client: OrderClient):
        self.price_data_controller = price_data_controller
        self.strategy_proc = strategy_proc
        self.order_controller = order_controller
        self.position_data_controller = position_data_controller
        self.order_history = order_history
        self.account_data = account_data
        self.order_client = order_client


class BTExchange:
    def __init__(self,
                 price_stream: PriceStream,
                 trade_manager: TradeManager,
                 broker: BackTestBroker,
                 order_receiver: NewOrderReceiver):
        self.price_stream = price_stream
        self.trade_manager = trade_manager
        self.broker = broker
        self.order_receiver = order_receiver


# TODO: optimize statistical calculations of trade results
class BTTrader:
    def __init__(self, cl: BTClient, ex: BTExchange):
        self.cl = cl
        self.ex = ex
        self.__construct_client()
        self.__construct_exchange()
        self.__connect_client_to_exchange()

    def add_strategy(self, strategy: Union[Strategy, List[Strategy]]):
        if type(strategy) is list:
            [self.cl.strategy_proc.add(s) for s in strategy]
        else:
            self.cl.strategy_proc.add(strategy)

    def remove_strategy(self, strategy: Union[Strategy, List[Strategy]]):
        if type(strategy) is list:
            [self.cl.strategy_proc.remove(s) for s in strategy]
        else:
            self.cl.strategy_proc.remove(strategy)

    def start(self):
        self.ex.price_stream.start_feed()

    @lru_cache
    def trade_history(self) -> List[Trade]:
        return self.ex.trade_manager.trade_history

    @lru_cache
    def long_trades(self) -> List[Trade]:
        return [t for t in self.trade_history() if t.is_long]

    @lru_cache
    def short_trades(self) -> List[Trade]:
        return [t for t in self.trade_history() if not t.is_long]

    @lru_cache
    def winning_trades(self) -> List[Trade]:
        return [t for t in self.trade_history() if t.pl > 0]

    @lru_cache
    def losing_trades(self) -> List[Trade]:
        return [t for t in self.trade_history() if t.pl < 0]

    @lru_cache
    def long_winning_trades(self) -> List[Trade]:
        return [t for t in self.long_trades() if t.pl > 0]

    @lru_cache
    def long_losing_trades(self) -> List[Trade]:
        return [t for t in self.long_trades() if t.pl < 0]

    @lru_cache
    def short_winning_trades(self) -> List[Trade]:
        return [t for t in self.short_trades() if t.pl > 0]

    @lru_cache
    def short_losing_trades(self) -> List[Trade]:
        return [t for t in self.short_trades() if t.pl < 0]

    @lru_cache
    def pls(self) -> List[Decimal]:
        return [t.pl for t in self.trade_history()]

    @lru_cache
    def total_profit(self) -> Decimal:
        return sum([t.pl for t in self.winning_trades()])

    @lru_cache
    def total_loss(self) -> Decimal:
        return sum([t.pl for t in self.losing_trades()])

    @lru_cache
    def total_pl(self) -> Decimal:
        return self.total_profit() + self.total_loss()

    @lru_cache
    def n_wins(self) -> int:
        return len(self.winning_trades())

    @lru_cache
    def n_losses(self) -> int:
        return len(self.losing_trades())

    @lru_cache
    def n_evens(self) -> int:
        return self.n_trades() - self.n_wins() - self.n_losses()

    @lru_cache
    def n_trades(self) -> int:
        return len(self.trade_history())

    @lru_cache
    def percent_profitable(self) -> float:
        return len(self.winning_trades()) / self.n_trades()

    @lru_cache
    def max_winning_trade(self) -> Optional[Trade]:
        if self.n_wins():
            return sorted(self.winning_trades(),
                          key=lambda t: t.pl, reverse=True)[0]
        else:
            return None

    @lru_cache
    def max_losing_trade(self) -> Optional[Trade]:
        if self.n_wins():
            return sorted(self.losing_trades(),
                          key=lambda t: t.pl)[0]
        else:
            return None

    def __construct_client(self):
        self.cl.strategy_proc.add_order_observer(self.cl.order_controller)
        self.cl.price_data_controller.add_price_observer(self.cl.strategy_proc)

    def __construct_exchange(self):
        self.ex.order_receiver.add_order_observer(self.ex.broker)
        self.ex.broker.add_order_close_observer(self.ex.trade_manager)

    def __connect_client_to_exchange(self):
        self.ex.price_stream.add_price_observer(self.cl.price_data_controller)
        self.cl.order_client.add_order_observer(self.ex.order_receiver)

    def __destruct_client(self):
        self.cl.price_data_controller.remove_price_observer(
            self.cl.strategy_proc)
        self.cl.strategy_proc.remove_order_observer(self.cl.order_controller)

    def __destruct_exchange(self):
        pass

    def __disconnect_client_from_exchange(self):
        self.ex.price_stream.remove_price_observer(
            self.cl.price_data_controller)
        self.cl.order_client.remove_order_observer(self.ex.broker)
