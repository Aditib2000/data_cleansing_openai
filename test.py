import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    if db.is_connected():
        db.close()
        print("Success: Database connected correctly!")
        
except Exception as e:
    print(f"Connection Failed: {e}")