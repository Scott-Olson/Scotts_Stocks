import secrets
import sqlite3
import alpaca_trade_api as tradeapi
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


API_KEY = secrets.API_KEY
SECRET_KEY = secrets.SECRET_KEY
ENDPOINT = secrets.BASE_URL
DB_FILE = secrets.DB_FILE

app = FastAPI()
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=ENDPOINT)
templates = Jinja2Templates(directory="templates")


def fetch_current_symbols():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # fetch the rows from the db
    cursor.execute("""
        SELECT symbol, name FROM stock
    """)
    rows = cursor.fetchall()
    # return all the symbols
    symbols = [(row['symbol'], row['name']) for row in rows]

    return symbols


# decorator from fast api routing.
@app.get("/")
def index():
    symbols = fetch_current_symbols()
    return {"title": "Dashboard", "stocks": symbols}
