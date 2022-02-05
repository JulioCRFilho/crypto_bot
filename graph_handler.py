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
        # plt.ion()z
        # self.ani = FuncAnimation(plt.gcf(), self.animate, interval=1000)
        # plt.pause(0.0001)
        plt.show(block=False)

    def update_trader(self, candle):
        self.trader.update(candle)

    def animate(self):
        plt.cla()
        print(f'last {self.df.closeTime.head(1)}')
        plt.plot(self.df.closeTime.tail(15), self.df.close.tail(15))
        plt.draw()
        plt.pause(0.0001)

    def update_df(self, new_df):
        self.df.append(new_df, ignore_index=True)
        self.animate()
