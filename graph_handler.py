import pandas as pd

from pandas import DataFrame

from trader import Trader
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#%matplotlib qt

plt.style.use('fivethirtyeight')


class GraphHandler:
    df = ani = trader = None

    def __init__(self, df: DataFrame):
        self.df = df
        self.trader = Trader()
        self.main()

    def main(self):
        self.ani = FuncAnimation(plt.gcf(), self.animate, interval=1000)

        plt.tight_layout()
        plt.show()

    def update_trader(self, candle):
        self.trader.update(candle)

    def animate(self, i):
        plt.cla()
        plt.plot(self.df.closeTime.tail(10), self.df.close.tail(10))

    def update_df(self, new_df):
        print(f'atualizou {new_df.close}')
        self.df.append(new_df)

