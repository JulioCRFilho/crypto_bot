def map_dataframe(json):
    return {'dateTime': json.get('t'), 'open': json.get('o'), 'high': json.get('h'), 'low': json.get('l'),
            'close': json.get('c'), 'volume': json.get('v'), 'closeTime': json.get('T')}
