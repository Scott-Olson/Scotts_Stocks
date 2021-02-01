import sqlite3

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

cursor.execute("DELETE FROM stock")

connection.commit()