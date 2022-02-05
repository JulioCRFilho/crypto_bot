import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas import DataFrame

plt.style.use('fivethirtyeight')


class GraphHandler:
    df = ani = trader = None

    def __init__(self, df: DataFrame):
        self.df = df
        # self.trader = Trader()
        self.main()

    def main(self):
        self.ani = FuncAnimation(plt.gcf(), self.animate, interval=1000)
        plt.ion()
        plt.pause(0.001)

    def update_trader(self, candle):
        self.trader.update(candle)

    def animate(self, i):
        plt.cla()
        plt.plot(self.df.closeTime.tail(15), self.df.close.tail(15))
        plt.pause(0.001)

    def update_df(self, new_df):
        self.df.append(new_df)
