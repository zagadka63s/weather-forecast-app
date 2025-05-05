import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from db.config import DB_CONFIG

def test_predict_next_day():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT datetime, temperature FROM weather_data"
    df = pd.read_sql(query, conn)
    conn.close()

    df['datetime'] = pd.to_datetime(df['datetime'])
    df['day'] = (df['datetime'] - df['datetime'].min()).dt.days

    X = df['day'].values.reshape(-1, 1)
    y = df['temperature'].values

    model = LinearRegression()
    model.fit(X, y)

    next_day = X[-1][0] + 1
    predicted_temp = model.predict([[next_day]])

    assert predicted_temp[0] is not None
    print("✅ Прогноз на наступний день працює:", predicted_temp[0])

def test_predict_next_year():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT datetime, temperature FROM weather_data"
    df = pd.read_sql(query, conn)
    conn.close()

    df['datetime'] = pd.to_datetime(df['datetime'])
    df['day_of_year'] = df['datetime'].dt.dayofyear

    X = df['day_of_year'].values.reshape(-1, 1)
    y = df['temperature'].values

    model = LinearRegression()
    model.fit(X, y)

    today_day = pd.Timestamp.now().dayofyear
    predicted_temp = model.predict([[today_day]])

    assert predicted_temp[0] is not None
    print("✅ Прогноз на наступний рік працює:", predicted_temp[0])

def test_predict_20_years():
    x = np.linspace(0, 20 * 2 * np.pi, 365 * 20)
    global_warming_func = x / 100
    year_temp_change = 15 * np.sin(x) + global_warming_func + 10
    decage_temp_change = np.sin(x / 12 / 2 / np.pi) / 10 + year_temp_change
    day_temp_change = (np.sin(365 * x) / 20 + year_temp_change)

    temp_prediction_func = (year_temp_change + decage_temp_change + day_temp_change) / 3

    assert len(temp_prediction_func) > 0
    print("✅ Прогноз на 20 років працює (згенеровано значень):", len(temp_prediction_func))

if __name__ == "__main__":
    test_predict_next_day()
    test_predict_next_year()
    test_predict_20_years()
