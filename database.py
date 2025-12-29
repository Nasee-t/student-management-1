import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

def get_cursor():
    return db.cursor(dictionary=True)

def commit():
    db.commit()
