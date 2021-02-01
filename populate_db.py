import sqlite3
import secrets

API_KEY = secrets.api_key
SECRET_KEY = secrets.secret_key
ENDPOINT = secrets.endpoint

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

connection.commit()