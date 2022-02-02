from binance.enums import *
from pandas import DataFrame


class Trader:
    df = None

    def __init__(self):
        self.df = DataFrame()
        self.main()

    def main(self):
        pass

    def update(self, candle):
        pass

    def make_order(self, client, qtd, coin_symbol, sell: bool):
        order = client.create_test_order(
            symbol=coin_symbol,
            side=SIDE_SELL if sell else SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=qtd,
        )
        print('sucesso!' if order == {} else 'falhou!')
        return order
