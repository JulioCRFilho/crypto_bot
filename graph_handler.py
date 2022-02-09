import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame
import mplfinance as mpl


plt.style.use('ggplot')


class GraphHandler:
    df = trader = ohlc = fig = ax = coin_symbol = None

    def __init__(self, df: DataFrame, coin_symbol: str):
        self.df = df
        self.coin_symbol = coin_symbol
        # self.trader = Trader()
        self.main()

    def main(self):
        self.df.index.name = 'Date'
        self.df.dateTime = pandas.DatetimeIndex(self.df.closeTime)
        self.df.set_index('dateTime', inplace=True)
        self.df.open = self.df.open.astype(float)
        self.df.high = self.df.high.astype(float)
        self.df.low = self.df.low.astype(float)
        self.df.close = self.df.close.astype(float)
        self.df.volume = self.df.volume.astype(float)

        mc = mpl.make_marketcolors(up='g', down='r')
        s = mpl.make_mpf_style(marketcolors=mc)
        mpl.plot(self.df.tail(30), type='candle', style=s)

    def update_trader(self, candle):
        self.trader.update(candle)

    def animate(self):
        # plt.cla()
        # self.bp = self.ax.boxplot(self.df)
        plt.pause(0.0001)

    def update_df(self, new_df):
        self.df = self.df.append(new_df, ignore_index=True)
        self.animate()
