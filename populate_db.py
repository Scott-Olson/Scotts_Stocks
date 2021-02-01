import sqlite3
import secrets
import alpaca_trade_api as tradeapi

# import for testing
import sys

# api secrets
API_KEY = secrets.api_key
SECRET_KEY = secrets.secret_key
ENDPOINT = secrets.endpoint

# set up databse connection
connection = sqlite3.connect('app.db')
cursor = connection.cursor()

# instantiate trade api
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url = ENDPOINT)


assets = api.list_assets()

print(sys.getsizeof(assets) / 1024)
print(len(assets))





connection.commit()