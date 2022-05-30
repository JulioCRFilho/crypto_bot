from binance.enums import *
from pandas import DataFrame


class Position(Enum):
    fst_p = 1
    fst_n = 2
    sec_p = 3
    sec_n = 4


def make_order(client, qtd, coin_symbol, sell: bool):
    order = client.create_test_order(
        symbol=coin_symbol,
        side=SIDE_SELL if sell else SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=qtd,
    )
    print('sucesso!' if order == {} else 'falhou!')
    return order


class Trader:
    last_filled: Position = None

    first_positive = first_negative = second_positive = second_negative = []

    df = None

    def __init__(self, df: DataFrame):
        self.df = df

    def update(self, new_df: DataFrame):
        self.df = self.df.append(new_df)
        self.validate()

    def validate(self):
        if self.df.iloc[-1].close == self.df.iloc[-2].close:
            pass
        else:
            self.select()

    def select(self):
        if self.last_filled is None:
            self.fill(Position.fst_p)

        elif self.last_filled is Position.fst_p:
            if self.df.iloc[-1].close > self.first_positive[-1].close:
                self.fill(Position.fst_p)
            else:
                self.fill(Position.fst_n)

        elif self.last_filled is Position.fst_n:
            if self.df.iloc[-1].close < self.first_negative[-1].close:
                self.fill(Position.fst_n)
            else:
                self.fill(Position.sec_p)

        elif self.last_filled is Position.sec_p:
            if self.df.iloc[-1].close < self.second_positive[-1].close:
                self.fill(Position.sec_p)
            else:
                self.fill(Position.sec_n)

        elif self.last_filled is Position.sec_n:
            if self.df.iloc[-1].close < self.second_negative[-1].close:
                self.fill(Position.sec_n)
            else:
                # make decision or reset
                pass

        else:
            pass

    def fill(self, which: Position):
        if which is Position.fst_p:
            self.first_positive.append(self.df.iloc[-1].close)

        elif which is Position.fst_n:
            self.first_negative.append(self.df.iloc[-1].close)

        elif which is Position.sec_p:
            self.second_positive.append(self.df.iloc[-1].close)

        elif which is Position.sec_n:
            self.second_negative.append(self.df.iloc[-1].close)

        else:
            pass

        self.last_filled = which
