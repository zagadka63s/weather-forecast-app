import mysql.connector
from db.config import DB_CONFIG


CSV_FILE = "weather_data.csv"

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

with open(CSV_FILE, 'r', encoding='utf-8') as file:
    
    for _ in range(9):
        next(file)

    for line in file:
        parts = line.strip().split(',')
        if len(parts) < 2:
            continue

        timestamp_raw = parts[0]
        temperature = parts[1]

        
        from datetime import datetime

        dt = datetime.strptime(timestamp_raw, "%Y%m%dT%H%M")
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')

        
        cursor.execute("""
            INSERT INTO weather_data (datetime, temperature)
            VALUES (%s, %s)
        """, (dt_str, temperature))

conn.commit()
print("Дані успішно завантажено.")

cursor.close()
conn.close()
