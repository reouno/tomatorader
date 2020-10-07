from decimal import Decimal
from logging import getLogger
from pathlib import Path

import numpy as np
import pandas as pd

from tmtrader.entity.price import Bar, DefaultPriceSequence, PriceSequence
from tmtrader.exchange_for_backtest.price_stream import PriceStream
from tmtrader.usecase.round_price import RoundPrice

logger = getLogger(__name__)

# FIXME: set this value at configuration
N_PAST_BARS = 10

# FIXME: set these values based on the focused product
# These are the configurations for "Micro E-Mini S&P 500 Futures"
MIN_FRAC = 25
N_FLOAT_DIGITS = 2


class CSVPriceDataFeeder(PriceStream):
    @staticmethod
    def _read_csv(file_path: Path):
        df = pd.read_csv(file_path)
        _validate_data_layout(df)
        return df.to_numpy()

    def __init__(self, file_path: Path, rounder: RoundPrice):
        super().__init__()
        self.__price_seq = self._read_csv(file_path)
        self.__n_past_bars = N_PAST_BARS
        self.__current_bar_idx = self.__n_past_bars
        self.__rounder = rounder

    def start_feed(self):
        seq_len = self.__price_seq.shape[0]
        if seq_len < self.__n_past_bars:
            logger.warning(
                f'Not enough data to use. The length of the historical data '
                f'`{seq_len}` is smaller than the number of '
                f'past bars to use `{self.__n_past_bars}`.')
            return

        for idx in range(self.__n_past_bars - 1, seq_len):
            logger.debug(f'{idx:08d} / {seq_len:08d}')
            start = idx - (self.__n_past_bars - 1)
            self.__current_bar_idx = idx + 1
            seq = np.flipud(self.__price_seq[start:self.__current_bar_idx])
            self._notify_price_update(DefaultPriceSequence(seq))

    def get_latest_bars(self, n_bars: int = 1) -> PriceSequence:
        if n_bars > self.__current_bar_idx:
            raise ValueError(
                f'n_bars (={n_bars}) must be smaller or equal to '
                f'self.__current_bar_idx (={self.__current_bar_idx}).')
        elif n_bars < 1:
            raise ValueError(
                f'n_bars must be a value of positive int larger or equal to '
                f'1, but got {n_bars}.')

        start = self.__current_bar_idx - n_bars

        return DefaultPriceSequence(
            np.flipud(self.__price_seq[start:self.__current_bar_idx]))

    def get_latest_bar_decimal(self) -> Bar:
        bar = self.get_latest_bars(1)
        return Bar(self.__rounder.round2fraction(Decimal(bar.open[0])),
                   self.__rounder.round2fraction(Decimal(bar.high[0])),
                   self.__rounder.round2fraction(Decimal(bar.low[0])),
                   self.__rounder.round2fraction(Decimal(bar.close[0])),
                   int(bar.vol[0]),
                   int(bar.time[0]))


def _validate_data_layout(df: pd.DataFrame, headers=None):
    if headers is None:
        headers = ['Open', 'High', 'Low', 'Close', 'Vol', 'Time']

    if list(df.columns) != headers:
        raise ValueError(
            f'CSV file have the following headers and only them: {headers}')

    for col_name in df.columns:
        if df[col_name].dtype == object:
            raise ValueError(
                f'Element dtype of the column `{col_name}` is '
                f'{df[col_name].dtype}. All dtype must be number types.')
