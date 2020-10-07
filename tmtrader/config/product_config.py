from decimal import Decimal


class ConfigError(BaseException):
    pass


class ProductConfig:
    def __init__(self, product_id: int, raw: dict):
        self.__id = product_id
        self.__raw = raw

    @property
    def min_frac(self) -> Decimal:
        return Decimal(self.__prod['min_frac'])

    @property
    def n_float_digits(self) -> int:
        return int(self.__prod['n_float_digits'])

    @property
    def __prod(self) -> dict:
        products = self.__raw['products']
        try:
            return [p for p in products if p['id'] == self.__id][0]
        except IndexError:
            raise ConfigError(
                f'product id `{self.__id}` is not found in the product config.')
