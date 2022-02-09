import asyncio
import pandas as pd
import atexit
from datetime import datetime
from binance import Client, BinanceSocketManager, AsyncClient
from constants import get_api_key, get_secret_key
from graph_handler import GraphHandler
from utils import map_kline


class CryptoBot:
    def __init__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())

    coin_symbol = investment_value = initial_investment = BSM = ts = client = in_position = graph_handler = None

    async def main(self):
        atexit.register(self.exit_handler)

        self.coin_symbol = 'BTCUSDT'  # input('Insira o símbolo da moeda que deseja negociar: ')
        self.investment_value = 50  # float(input('Insira o valor que deseja investir em dolar: '))
        self.initial_investment = self.investment_value

        key = get_api_key()
        secret = get_secret_key()

        self.client = await AsyncClient.create(api_key=key, api_secret=secret)
        self.BSM = BinanceSocketManager(self.client)

        history = await self.client.get_historical_klines(self.coin_symbol, Client.KLINE_INTERVAL_1MINUTE,
                                                          str(datetime.now()))

        df = pd.DataFrame(history, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
                                            'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol',
                                            'takerBuyQuoteVol', 'ignore'])

        df = df.drop(
            columns=['quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])

        df.closeTime = pd.to_datetime(df.closeTime, unit='ms')
        df.close = df.close.astype(float)

        self.graph_handler = GraphHandler(df, self.coin_symbol)
        self.ts = self.BSM.kline_socket(self.coin_symbol)

        await self.handle_socket()

    async def handle_socket(self):
        async with self.ts as live:
            while True:
                msg = await live.recv()
                mapped = map_kline(msg['k'])
                new_df = pd.DataFrame(mapped, index=[mapped['closeTime']],
                                      columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime'])

                new_df.closeTime = pd.to_datetime(new_df.closeTime, unit='ms')
                new_df.close = new_df.close.astype(float)

                if new_df is None:
                    print('new_df is None')
                    return

                if self.investment_value <= 0 and self.in_position is None:
                    self.client.close_connection()
                    self.graph_handler = None
                    print('bot stopped due to lacking of investment, sorry for your lost :(')

                else:
                    if self.graph_handler is not None:
                        self.graph_handler.update_df(new_df)

    def exit_handler(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.kill_connection())

    async def kill_connection(self):
        await self.client.close_connection()

