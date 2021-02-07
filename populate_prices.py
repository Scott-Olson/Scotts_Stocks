import secrets
import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(secrets.DB_FILE)

# returns Row objects rather than tuples for easy manipulation
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

api = tradeapi.REST(secrets.API_KEY, secrets.SECRET_KEY,
                    base_url=secrets.BASE_URL)

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

symbols = []

stock_dict = {}

# creates a lookup table to use when entering stock data by foregin key later
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']


# alapaca allows for calls up 200 in size, use this as our chunk size
# reduces api calls needed
chunk_size = 200
added = 0
for i in range(0, len(symbols), chunk_size):
    # grabs all the chunked symbols in our saved list
    symbol_chunk = symbols[i: i+chunk_size]

    barsets = api.get_barset(symbol_chunk, 'day')

    for symbol in barsets:
        print(f"Processing: {symbol} ...")
        for bar in barsets[symbol]:
            # use look up table to get stock id for foreign key
            stock_id = stock_dict[symbol]

            cursor.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
        added += 1

print(f"{added} symbols added")

connection.commit()
