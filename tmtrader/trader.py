import json
from logging import getLogger
from pathlib import Path
from typing import List, Union

from tmtrader.api.back_test.order_client import BackTestOrderClient
from tmtrader.api.back_test.order_manager_client import BTOrderManagerClient
from tmtrader.api.back_test.position_client import PositionClient
from tmtrader.back_test_trader import BTClient, BTExchange, BTTrader
from tmtrader.config.product_config import ProductConfig
from tmtrader.controller.account_data_controller import BTAccountDataController
from tmtrader.controller.order_controller import DefaultOrderController
from tmtrader.controller.order_history_controller import \
    BTOrderHistoryController
from tmtrader.controller.price_data_controller import BTPriceDataController
from tmtrader.controller.strategy_processor import StrategyProcessor
from tmtrader.controller.position_data_controller import \
    BTPositionDataController
from tmtrader.exchange_for_backtest.back_test_broker import BackTestBroker
from tmtrader.exchange_for_backtest.csv_price_data_feeder import \
    CSVPriceDataFeeder
from tmtrader.exchange_for_backtest.new_order_receiver import NewOrderReceiver
from tmtrader.exchange_for_backtest.order_manager import OrderManager
from tmtrader.exchange_for_backtest.position_manager import PositionManager
from tmtrader.exchange_for_backtest.trade_manager import TradeManager
from tmtrader.exchange_for_backtest.usecase.one_order_spec import OneOrderSpec
from tmtrader.usecase.round_price import RoundPrice

logger = getLogger(__name__)

# TODO: set this value at configuration
PRODUCT_ID = 1  # Micro E-Mini S&P 500 Futures


def _create_single_data_trader(file_path: str, raw_product_config: dict, *args,
                               **kwargs) -> BTTrader:
    product_conf = ProductConfig(PRODUCT_ID, raw_product_config)

    # exchange
    price_seq_feeder = CSVPriceDataFeeder(Path(file_path),
                                          RoundPrice(product_conf))
    position_mng = PositionManager()
    order_mng = OrderManager()
    trade_manager = TradeManager(position_mng, order_mng)
    broker = BackTestBroker(price_seq_feeder)
    order_receiver = NewOrderReceiver()
    bt_exchange = BTExchange(price_seq_feeder, trade_manager, broker,
                             order_receiver)

    # client
    order_mng_client = BTOrderManagerClient(order_mng)
    order_history = BTOrderHistoryController(order_mng_client)
    order_spec = OneOrderSpec(order_history)
    price_data_controller = BTPriceDataController()
    order_client = BackTestOrderClient()
    order_controller = DefaultOrderController(order_client, order_spec)
    position_client = PositionClient(position_mng)
    position_data_controller = BTPositionDataController(position_client)
    account_data = BTAccountDataController()
    strategy_proc = StrategyProcessor(position_data_controller)
    bt_client = BTClient(price_data_controller,
                         strategy_proc,
                         order_controller,
                         position_data_controller,
                         order_history,
                         account_data,
                         order_client)

    return BTTrader(bt_client, bt_exchange)


# TODO: implement
def _create_multi_data_trader(file_paths: List[str], raw_product_config: dict,
                              *args, **kwargs) -> BTTrader:
    logger.warning('create_multi_data_trader() is not implemented yet.')
    raise NotImplementedError(
        'create_multi_data_trader() is not implemented yet.')


def create_trader(file_paths: Union[str, List[str]], product_config_file: str,
                  *args, **kwargs) -> BTTrader:
    with open(product_config_file, mode='r') as f:
        raw_product_config = json.load(f)
    if isinstance(file_paths, str):
        return _create_single_data_trader(file_paths, raw_product_config,
                                          *args, **kwargs)
    else:
        return _create_multi_data_trader(file_paths, raw_product_config, *args,
                                         **kwargs)
