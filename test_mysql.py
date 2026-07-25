import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

print("HOST:", os.getenv("MYSQLHOST"))
print("PORT:", os.getenv("MYSQLPORT"))

conn = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)

print("MYSQL CONNECTED SUCCESSFULLY")

conn.close()