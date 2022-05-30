import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame
import mplfinance as mpl


plt.style.use('ggplot')


class GraphHandler:
    df = ohlc = fig = s = coin_symbol = None

    def __init__(self, df: DataFrame, coin_symbol: str):
        self.df = df
        self.coin_symbol = coin_symbol
        # self.trader = Trader()
        self.main()

    def main(self):
        self.df = self.format_df(self.df)

        mc = mpl.make_marketcolors(up='g', down='r')
        self.s = mpl.make_mpf_style(marketcolors=mc)
        mpl.plot(self.df.tail(30), type='candle', style=self.s)

    def update_df(self, new_df):
        formatted = self.format_df(new_df)
        self.df = self.df.append(formatted)
        mpl.make_addplot(formatted)

    def format_df(self, df):
        df.index.name = 'Date'
        df.dateTime = pandas.DatetimeIndex(self.df.closeTime)
        df.set_index('dateTime', inplace=True)
        df.open = self.df.open.astype(float)
        df.high = self.df.high.astype(float)
        df.low = self.df.low.astype(float)
        df.close = self.df.close.astype(float)
        df.volume = self.df.volume.astype(float)
        return df
