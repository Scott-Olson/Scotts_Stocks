import secrets
import alpaca_trade_api as tradeapi

api = tradeapi.REST(secrets.API_KEY, secrets.SECRET_KEY, base_url = secrets.BASE_URL)

barsets = api.get_barset(['Z'], 'minute')


for symbol in barsets:
    print(f"Processing symbol: {symbol}")

    for bar in barsets[symbol]:
        # time, open, high, low, close, volume
        print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)