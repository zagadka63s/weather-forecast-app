import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from db.config import DB_CONFIG

st.set_page_config(page_title="🌦️ Прогноз погоди", page_icon="🌦️")

st.title("🌦️ Прогноз погоди - Аналітика та Майбутнє")

option = st.selectbox(
    '🔎 Виберіть тип прогнозу:',
    ('Прогноз на наступний день', 'Прогноз на наступний рік', 'Прогноз на 20 років')
)

def format_temperature(temp):
    if temp <= 5:
        return f"❄️ Дуже холодно: {temp:.2f}°C"
    elif 5 < temp <= 20:
        return f"🌤️ Помірно: {temp:.2f}°C"
    else:
        return f"🔥 Спекотно: {temp:.2f}°C"

if option == 'Прогноз на наступний день':
    st.header("📅 Прогноз на наступний день")

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
    next_date = df['datetime'].max() + timedelta(days=1)

    st.success(f"Дата прогнозу: {next_date.strftime('%Y-%m-%d')} — {format_temperature(predicted_temp[0])}")
    st.info("Це прогноз на основі моделі машинного навчання. Точність залежить від наявних історичних даних.")

elif option == 'Прогноз на наступний рік':
    st.header("📅 Прогноз на наступний рік")

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

    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    next_year_date = today + timedelta(days=365)

    predicted_temp = model.predict([[day_of_year]])

    st.success(f"Дата прогнозу: {next_year_date.strftime('%Y-%m-%d')} — {format_temperature(predicted_temp[0])}")
    st.info("Прогноз базується на річних трендах та сезонності.")

elif option == 'Прогноз на 20 років':
    st.header("📅 Прогноз на 20 років вперед")

    def predict_temperature(year_number=20, global_warming_rate=100, year_cycles=12, temperature_change=15, axial_shift=10):
        x = np.linspace(0, year_number * 2 * np.pi, 365 * year_number)
        global_warming_func = x / global_warming_rate
        year_temp_change = temperature_change * np.sin(x) + global_warming_func + axial_shift
        decage_temp_change = np.sin(x / year_cycles / 2 / np.pi) / 10 + year_temp_change
        day_temp_change = (np.sin(365 * x) / 20 + year_temp_change)
        temp_prediction_func = (year_temp_change + decage_temp_change + day_temp_change) / 3
        return x, temp_prediction_func

    x, temp_prediction_func = predict_temperature()

    min_temp = np.min(temp_prediction_func)
    max_temp = np.max(temp_prediction_func)
    avg_temp = np.mean(temp_prediction_func)

    st.success(f"📈 Прогноз побудований! Мінімум: {min_temp:.2f}°C | Середнє: {avg_temp:.2f}°C | Максимум: {max_temp:.2f}°C")
    st.info("Це довгостроковий прогноз, побудований за допомогою математичних моделей та трендів.")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, temp_prediction_func, label='Прогноз 20 років')
    ax.set_xlabel("X (день)")
    ax.set_ylabel("Температура")
    ax.set_title("Прогноз температури на 20 років вперед")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
