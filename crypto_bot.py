import threading
import pandas as pd
from datetime import datetime
from binance import ThreadedWebsocketManager, Client
from constants import get_api_key, get_secret_key
from graph_handler import GraphHandler
from utils import map_dataframe


class CryptoBot:
    def __init__(self):
        self.main()

    coin_symbol = investment_value = initial_investment = twm = client = in_position = None

    first_positive = first_negative = second_positive = second_negative = last_filled = None

    first_candle = True

    binance_tax = .001

    graph_handler = None

    def main(self):
        self.coin_symbol = 'ETHUSDT'  # input('Insira o símbolo da moeda que deseja negociar: ')
        self.investment_value = 50  # float(input('Insira o valor que deseja investir em dolar: '))
        self.initial_investment = self.investment_value

        key = get_api_key()
        secret = get_secret_key()

        self.twm = ThreadedWebsocketManager(key, secret)
        self.twm.start()

        self.client = Client(key, secret)
        history = self.client.get_historical_klines(self.coin_symbol, Client.KLINE_INTERVAL_1MINUTE,
                                                    str(datetime.now()))

        df = pd.DataFrame(history, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
                                            'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol',
                                            'takerBuyQuoteVol', 'ignore'])

        df = df.drop(
            columns=['quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])

        df.closeTime = pd.to_datetime(df.closeTime, unit='ms')

        df.close = df.close.astype(float)

        self.graph_handler = GraphHandler(df)

        self.twm.start_kline_socket(callback=self.handle_socket, symbol=self.coin_symbol)

    # then start receiving messages
    def handle_socket(self, msg):
        print('handling socket...')
        candle = pd.json_normalize(msg['k'])
        mapped = map_dataframe(candle)
        new_df = pd.DataFrame(mapped, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime'])
        new_df.closeTime = pd.to_datetime(new_df.closeTime, unit='ms')
        new_df.close = new_df.close.astype(float)

        if new_df is None:
            print('new_df is None')
            return

        if self.investment_value <= 0 and self.in_position is None:
            self.twm.stop()
            print('bot stopped due to lacking of investment, sorry for your lost :(')

        else:
            if self.graph_handler is not None:
                self.graph_handler.update_df(new_df)
            else:
                print('graph_handler is None')
