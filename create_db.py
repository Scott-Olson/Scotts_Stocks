import sqlite3
import secrets

# DATA BASE SET UP SCRIPT
# creates a connection to the SQLite db
# if the database does not exist, it will be created
connection = sqlite3.connect(secrets.DB_FILE)

# a cursor object that has execute methods
cursor = connection.cursor()

# execute takes SQLite statements
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL
    )
""")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY,
        stock_id INTEGER, 
        date NOT NULL,
        open NOT NULL,
        high NOT NULL,
        low NOT NULL,
        close NOT NULL,
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    ) 
    """
)
# connection commit the current transaction
# if you commit each action, changes can be written and rolled back
connection.commit()
