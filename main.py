from logging import DEBUG, INFO, basicConfig, getLogger

from strategies.entry_buy_random import EntryBuyRandom
from strategies.exit_sell_in_n_bars import ExitSellInNBars
from strategies.exit_sell_with_target_profit import ExitSellWithTargetProfit
from strategies.monkey_strategy import MonkeyStrategy
from tmtrader.trader import create_trader

basicConfig(level=DEBUG)
logger = getLogger(__name__)


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows,
# actions, and settings.

def main():
    trader = create_trader('data/e-mini-sp500-daily-compact.csv',
                           'tmtrader/config/product_config.json')

    entry_buy1 = EntryBuyRandom(prob=0.5)
    exit_sell1 = ExitSellWithTargetProfit(target_profit=5)
    exit_sell2 = ExitSellInNBars(n_bars=5)
    trader.add_strategy([entry_buy1, exit_sell1, exit_sell2])

    trader.start()

    print(f'TNT: {len(trader.trade_history())}')

    print(f'Total P/L: {trader.total_pl()}')
    print(f'Total NO. of Trades: {trader.n_trades()}')
    print(f'Percent profitable: {trader.percent_profitable() * 100:.2f}%')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.debug('from logger')
    logger.info('from logger')
    logger.warning('from logger')
    logger.critical('from logger')
    logger.error('from logger')
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
