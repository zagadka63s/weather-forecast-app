import mysql.connector
from db.config import DB_CONFIG

def test_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print(" База даних підключена успішно!")
        conn.close()
    except Exception as e:
        print(" Помилка підключення до бази даних:", e)

if __name__ == "__main__":
    test_db_connection()
