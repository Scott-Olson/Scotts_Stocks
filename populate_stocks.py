import secrets
import sqlite3
import sys

import alpaca_trade_api as tradeapi

# api secrets
API_KEY = secrets.API_KEY
SECRET_KEY = secrets.SECRET_KEY
ENDPOINT = secrets.BASE_URL
DB_FILE = secrets.DB_FILE

# set up databse connection
connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


# instantiate trade api
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=ENDPOINT)

# list_assets returns all the market symbols
assets = api.list_assets()

print(sys.getsizeof(assets) / 1024)
print(len(assets))


def fetch_current_symbols(cursor):
    # fetch the rows from the db
    cursor.execute("""
        SELECT symbol, name FROM stock
    """)
    rows = cursor.fetchall()
    # return all the symbols
    symbols = [row['symbol'] for row in rows]

    return symbols


# retrieve the current symbols stored in the db
symbols = fetch_current_symbols(cursor)

for asset in assets:
    # structure the query and params as would be expected by SQLite3
    query = "INSERT INTO stock(symbol, name, exchange) VALUES (?, ?, ?)"
    params = (asset.symbol, asset.name, asset.exchange)
    try:
        # constrain the try to active and tradable stocks
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            # execute the query
            print(f"Inserting {asset.name} into db as {asset.symbol}.")
            cursor.execute(query, params)

    except Exception as e:
        print(f"Symbol: {asset.symbol}, Comapny: {asset.name}")
        print(e)


# save changes to the db
connection.commit()
