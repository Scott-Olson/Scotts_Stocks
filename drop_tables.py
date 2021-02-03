import sqlite3
import secrets


# RUN THIS WITH EXTREME CAUTION
connection = sqlite3.connect(secrets.DB_FILE)

cursor = connection.cursor()

print("Executing this script will drop your stock tables, are you sure you want to continue? y/N")
i = input()

if i == "y" or i == "yes":
    # drop stock_price table
    cursor.execute(""" 
        DROP TABLE stock_price
    """)
    print("dropped stock_price table")

    # drop stock table
    cursor.execute(""" 
        DROP TABLE stock
    """)
    print("dropped stock table")

    connection.commit()
