import asyncio
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from binance import AsyncClient, BinanceSocketManager
from constants import API_KEY, API_SECRET

coin_symbol = 'SLPUSDT'
global moving_average_20
global moving_average_5
global current_price
global position_price
in_position = False
max_loss = .2
min_win = .8


async def main():
    client = await AsyncClient.create(API_KEY, API_SECRET)
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.kline_socket(coin_symbol)

    history = await client.get_historical_klines(coin_symbol, AsyncClient.KLINE_INTERVAL_1MINUTE, str(datetime.now()))
    df = pd.DataFrame(history, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
                                        'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol',
                                        'ignore'])

    df = df.drop(columns=['quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])

    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            candle = pd.json_normalize(res['k'])
            mapped = map_dataframe(candle)
            new_df = pd.DataFrame(mapped, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime'])
            df = df.append(new_df, ignore_index=True)
            pprint.pprint(df)


def map_dataframe(json):
    return {'dateTime': json.get('t'), 'open': json.get('o'), 'high': json.get('h'), 'low': json.get('l'),
            'close': json.get('c'), 'volume': json.get('v'), 'closeTime': json.get('T')}


def variation_over_1_percent():
    return current_price - moving_average_5 > moving_average_5 * .01


def take_action():
    if current_price > moving_average_20:
        should_sell()
    else:
        should_buy()


def should_sell():
    if not in_position:
        return

    loss_margin = (current_price - position_price) * max_loss
    if position_price <= current_price - loss_margin and variation_over_1_percent():
        print('should sell')
    else:
        print('should hold')


def should_buy():
    if in_position:
        return

    if current_price >= moving_average_5 and variation_over_1_percent():
        print('should buy')
    else:
        print('should wait')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
