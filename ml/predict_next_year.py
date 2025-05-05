import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from db.config import DB_CONFIG


conn = mysql.connector.connect(**DB_CONFIG)
query = "SELECT datetime, temperature FROM weather_data"
df = pd.read_sql(query, conn)
conn.close()

df['datetime'] = pd.to_datetime(df['datetime'])
df['day_of_year'] = df['datetime'].dt.dayofyear
df['year'] = df['datetime'].dt.year


X = df['day_of_year'].values.reshape(-1, 1)
y = df['temperature'].values


model = LinearRegression()
model.fit(X, y)


import datetime
today = datetime.datetime.now()
day_of_year = today.timetuple().tm_yday

predicted_temp = model.predict([[day_of_year]])
print(f"Прогноз температури на цей день через рік: {predicted_temp[0]:.2f}°C")
