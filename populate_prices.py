import secrets
import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(secrets.DB_FILE)

# returns Row objects rather than tuples for easy manipulation
connection.row_factory = sqlite3.Row

api = tradeapi.REST(secrets.API_KEY, secrets.SECRET_KEY,
                    base_url=secrets.BASE_URL)

barsets = api.get_barset(['Z'], 'minute')


for symbol in barsets:
    print(f"Processing symbol: {symbol}")

    for bar in barsets[symbol]:
        # time, open, high, low, close, volume
        print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)
