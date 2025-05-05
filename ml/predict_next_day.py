import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta
from db.config import DB_CONFIG


conn = mysql.connector.connect(**DB_CONFIG)
query = "SELECT datetime, temperature FROM weather_data"
df = pd.read_sql(query, conn)
conn.close()


df['datetime'] = pd.to_datetime(df['datetime'])
df['day'] = (df['datetime'] - df['datetime'].min()).dt.days
df = df.sort_values('day')

X = df['day'].values.reshape(-1, 1)
y = df['temperature'].values


model = LinearRegression()
model.fit(X, y)


next_day = X[-1][0] + 1
predicted_temp = model.predict([[next_day]])

print(f"Прогноз температури на наступний день: {predicted_temp[0]:.2f}°C")
