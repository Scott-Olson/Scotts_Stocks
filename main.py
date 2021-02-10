import secrets
import sqlite3
import alpaca_trade_api as tradeapi
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import date


API_KEY = secrets.API_KEY
SECRET_KEY = secrets.SECRET_KEY
TRADE_ENDPOINT = secrets.BASE_URL
DATA_ENDPOINT = secrets.DATA_URL
DB_FILE = secrets.DB_FILE

app = FastAPI()
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=TRADE_ENDPOINT)
templates = Jinja2Templates(directory="templates")

# returns current date in ISO format
# can be used later to alter if for queries if need be
# should check for weekend as well?? revert to closest trading day??


def get_todays_date_ISO():
    return date.today().isoformat()


def fetch_current_symbols() -> list:
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # fetch the rows from the db
    cursor.execute("""
        SELECT id, symbol, name FROM stock ORDER BY symbol
    """)
    rows = cursor.fetchall()
    # return all the symbols
    # symbols = [(row['symbol'], row['name']) for row in rows]

    return rows


def fetch_single_stock(symbol: str):
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # fetch the rows from the db
    cursor.execute("""
        SELECT id, symbol, name, exchange FROM stock where symbol = ? 
    """, (symbol,))
    row = cursor.fetchone()
    return row


def fetch_stock_historic_price(symbol: str, id: int):
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC
    """, (id, ))
    rows = cursor.fetchall()

    return rows

# query to fetch trading strategies


def get_strategies():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM strategy
     """)

    rows = cursor.fetchall()

    return rows


def get_strategy_by_id(id: int):
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, description FROM strategy WHERE id = ?
    """, (id,))
    row = cursor.fetchone()
    return row


def get_stocks_by_strategy(strategy_id: int):
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT symbol, name FROM stock JOIN stock_strategy ON stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
    """, (strategy_id,))
    rows = cursor.fetchall()
    return rows


def fetch_stock_current_price(symbol: str):
    # api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=DATA_ENDPOINT)
    return

# returns stocks that hit a new max close on specified date


def fetch_new_closing_pattern_stocks(direction: str):
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    print(f"Filtering closing to {direction}")

    if direction == "highs":
        cursor.execute("""
            SELECT * FROM (
                SELECT symbol, name, stock_id, max(close), date
                FROM stock_price JOIN stock ON stock.id = stock_price.stock_id
                GROUP BY stock_id
                ORDER BY symbol
            ) WHERE date = (SELECT max(date) FROM stock_price)
        """)
        rows = cursor.fetchall()
        return rows

    if direction == "lows":
        cursor.execute("""
            SELECT * FROM (
                SELECT symbol, name, stock_id, min(close), date
                FROM stock_price JOIN stock ON stock.id = stock_price.stock_id
                GROUP BY stock_id
                ORDER BY symbol
            ) WHERE date = (SELECT max(date) FROM stock_price)
        """)
        rows = cursor.fetchall()
        return rows

    else:
        print("Query params not valid, returning all stocks")
        return fetch_current_symbols()


# accepts the filter string, returns list of symbols by filter
def filter_stocks(stock_filter: str):
    if not stock_filter:
        symbols = fetch_current_symbols()

    if stock_filter == "new_intraday_highs":
        symbols = []
        print(f"Filtered to intraday highs len: {len(symbols)}")

    if stock_filter == "new_intraday_lows":
        symbols = []
        print(f"Filtered to intraday lows len: {len(symbols)}")

    if stock_filter == "new_closing_highs":
        symbols = fetch_new_closing_pattern_stocks("highs")
        print(f"Filtered to closing highs len: {len(symbols)}")

    if stock_filter == "new_closing_lows":
        symbols = fetch_new_closing_pattern_stocks("lows")
        print(f"Filtered to closing lows len: {len(symbols)}")

    return symbols


def validate_strategy_form_data(form_strat_id: str, form_stock_id: int, stock_id: int, symbol: str):
    stock_info = fetch_single_stock(symbol)

    return form_stock_id == stock_info['id'] == stock_id


@app.get("/")
def index(request: Request):
    # built in function in the Request object
    # allows for filtering/params without seperate routes
    # False is default in this function if no filter found
    stock_filter = request.query_params.get("filter", False)
    print(f"CURRENT FILTER: {stock_filter}")
    # applies current stock filter to symbols
    symbols = filter_stocks(stock_filter)
    strategies = get_strategies()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": symbols, "strategies": strategies, })


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol: str):
    # grab general stock info
    stock_info = fetch_single_stock(symbol)

    print(f"Fetching stock data for {stock_info['id']}: {symbol}")
    # call for stock prices
    price_data = fetch_stock_historic_price(symbol, stock_info['id'])

    strategies = get_strategies()

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock_info": stock_info, "price_data": price_data, "strategies": strategies})


@app.post("/stock/{symbol}/apply_strategy")
def apply_strategy(symbol: str, request: Request, strategy_id: int = Form(...), stock_id: int = Form(...)):

    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    stock_info = fetch_single_stock(symbol)

    form_valid = validate_strategy_form_data(
        strategy_id, stock_id, stock_info['id'], symbol)

    if form_valid:
        cursor.execute("""
            INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?, ?)
        """, (stock_id, strategy_id))

    connection.commit()

    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/strategy/{strategy_id}")
def strategy_landing(request: Request, strategy_id: int):
    strategies = get_strategies()
    strategy = get_strategy_by_id(strategy_id)

    stocks = get_stocks_by_strategy(strategy_id)

    return templates.TemplateResponse("strategy_detail.html", {"request": request, "strategies": strategies, "current_strat": strategy, "stocks": stocks})
