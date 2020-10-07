from decimal import Decimal
from itertools import product
from logging import INFO, basicConfig, getLogger
from typing import List, NamedTuple

import numpy as np
import pandas as pd
from deprecated import deprecated

from strategies.entry_buy_random import EntryBuyRandom
from strategies.exit_sell_in_n_bars import ExitSellInNBars
from strategies.exit_sell_with_target_profit import ExitSellWithTargetProfit
from tmtrader.entity.trade import Trade
from tmtrader.trader import create_trader
from tmtrader.usecase.strategy import Strategy

basicConfig(level=INFO)
logger = getLogger(__name__)


class TradeResult(NamedTuple):
    total_pl: Decimal
    total_profit: Decimal
    total_loss: Decimal
    n_trades: int
    n_wins: int
    n_losses: int
    percent_profitable: float
    max_prof_in1: Decimal
    max_loss_in1: Decimal
    trades: List[Trade]


class StrategyEvaluator:
    def __init__(self,
                 f_path: str,
                 product_config_file: str,
                 strategies: List[Strategy]):
        self.__f_path = f_path
        self.__p_conf_file = product_config_file
        self.__strategies = strategies
        self.__results: List[TradeResult] = list()

    def run(self, times: int = 10):
        self.__results = []
        for i in range(times):
            # FIXME: do not create trader every time
            #        define a method to clear all data in trader to reuse
            trader = self.__create_trader()
            trader.start()

            max_prof_in1 = trader.max_winning_trade().pl if \
                trader.max_winning_trade() else 0
            max_loss_in1 = trader.max_losing_trade().pl if \
                trader.max_losing_trade() else 0
            self.__results.append(
                TradeResult(trader.total_pl(),
                            trader.total_profit(),
                            trader.total_loss(),
                            trader.n_trades(),
                            trader.n_wins(),
                            trader.n_losses(),
                            trader.percent_profitable(),
                            max_prof_in1,
                            max_loss_in1,
                            trader.trade_history())
            )
            print(f'\r{i + 1:06d} / {times:06d}', end='')
        print()  # line feed

    @property
    def results(self):
        return self.__results

    def results_df(self):
        df = pd.DataFrame(
            {
                'pl': [float(t.total_pl) for t in self.__results],
                'profit': [float(t.total_profit) for t in self.__results],
                'loss': [float(t.total_loss) for t in self.__results],
                'n_trades': [t.n_trades for t in self.__results],
                'n_wins': [t.n_wins for t in self.__results],
                'n_losses': [t.n_losses for t in self.__results],
                'pp': [t.percent_profitable * 100 for t in self.__results],
                'pl_avg': [float(t.total_pl / t.n_trades) for t in
                           self.__results],
                'profit_avg': [float(t.total_profit / t.n_wins) for t in
                               self.__results],
                'loss_avg': [float(t.total_loss / t.n_losses) for t in
                             self.__results],
                'pf': [-float(t.total_profit / t.total_loss) for t in
                       self.__results],
                'max_prof_in1': [float(t.max_prof_in1) for t in
                                 self.__results],
                'max_loss_in1': [float(t.max_loss_in1) for t in
                                 self.__results],
            }
        )
        return df

    @deprecated
    def __create_trader(self):
        trader = create_trader(self.__f_path, self.__p_conf_file)
        trader.add_strategy(self.__strategies)
        return trader


def eval_random_strategy(prob: float,
                         target_prof: float,
                         exit_in_n_bars: int):
    entry_buy1 = EntryBuyRandom(prob=prob)
    exit_sell1 = ExitSellWithTargetProfit(target_profit=target_prof)
    exit_sell2 = ExitSellInNBars(n_bars=exit_in_n_bars)

    evaluator = StrategyEvaluator('data/e-mini-sp500-daily-compact.csv',
                                  'tmtrader/config/product_config.json',
                                  [entry_buy1,
                                   exit_sell1,
                                   exit_sell2])

    evaluator.run(30)

    return evaluator.results_df()


def main():
    # entry_probs = np.arange(0.3, 1, 0.3)
    entry_probs = [0.5]
    # target_profits = range(5, 51, 5)
    target_profits = list(range(25, 201, 25)) + [np.inf]
    # exit_in_n_barss = range(5, 61, 5)
    exit_in_n_barss = range(10, 201, 10)
    search_params = product(entry_probs, target_profits, exit_in_n_barss)
    df = pd.DataFrame()
    for i, (prob, target_prof, n_bars) in enumerate(search_params):
        df_tmp = eval_random_strategy(prob, target_prof, n_bars)
        df_tmp['sid'] = i
        df_tmp['entry_prob'] = prob
        df_tmp['target_prof'] = target_prof
        df_tmp['n_bars'] = n_bars
        df = pd.concat([df, df_tmp])

    df.to_csv('output/random_entry_target_profit_exit_in_n_bars.csv',
              index=False,
              float_format='%.2f')

    # pl = 0
    # for r in evaluator.results[0].trades:
    #     pl1 = r.exit.price - r.entry.price
    #     print(f'{r.exit.price: 10f}, {r.entry.price: 10f}, {pl1: 10f}')
    #     pl += pl1
    #
    # print(f'total PL = {pl}')


if __name__ == '__main__':
    main()
