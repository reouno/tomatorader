from decimal import Decimal

from tmtrader.config.product_config import ProductConfig


class RoundPrice:
    def __init__(self, product_conf: ProductConfig):
        self.__min_frac = product_conf.min_frac
        self.__n_float_digits = product_conf.n_float_digits

    def round2fraction(self, x: Decimal) -> Decimal:
        return round2fraction(x, self.__min_frac, self.__n_float_digits)


def round2fraction(x: Decimal, min_frac: Decimal,
                   n_float_digits: int) -> Decimal:
    """
    calculates a value rounded (round half up) to the nearest minmove fraction.
    :param x:
    :param min_frac:
    :param n_float_digits:
    :return:

    >>> round2fraction(Decimal('10.3749'), Decimal(25), 2)
    Decimal('10.25')
    >>> round2fraction(Decimal('10.375'), Decimal(25), 2)
    Decimal('10.5')
    """

    float_digis = 10 ** n_float_digits
    int_x = x * 10 ** n_float_digits
    int_x = int_x + min_frac / 2
    int_rounded = (int_x - int_x % min_frac).to_integral()
    return int_rounded / float_digis
