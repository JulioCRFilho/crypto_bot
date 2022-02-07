import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas import DataFrame

plt.style.use('fivethirtyeight')


class GraphHandler:
    df = ani = trader = fig = ax = bp = None

    def __init__(self, df: DataFrame):
        self.df = df
        # self.trader = Trader()
        self.main()

    def main(self):
        self.bp = plt.boxplot(self.df.candles, labels=self.df.time)
        plt.show(block=False)

    def update_trader(self, candle):
        self.trader.update(candle)

    def animate(self):
        # plt.cla()
        # self.bp = self.ax.boxplot(self.df.close)
        plt.pause(0.0001)

    def update_df(self, new_df):
        self.df = self.df.append(new_df, ignore_index=True)
        self.animate()
