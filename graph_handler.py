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
        plt.show(block=False)

    def update_trader(self, candle):
        self.trader.update(candle)

    def animate(self):
        # plt.cla()
        print(f'time: {self.df.tail(1).closeTime} && {self.df.tail(1).close}')
        plt.plot(self.df.tail(15).closeTime, self.df.tail(15).close)
        # plt.draw()
        plt.pause(0.0001)

    def update_df(self, new_df):
        self.df.append(new_df, ignore_index=True)
        self.animate()
