import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def get_cursor():
    db = get_db()
    return db, db.cursor(dictionary=True)

