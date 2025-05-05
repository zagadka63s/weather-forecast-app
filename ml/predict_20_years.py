import numpy as np
import matplotlib.pyplot as plt

def predict_temperature(year_number=20, global_warming_rate=100, year_cycles=12, temperature_change=15, axial_shift=10):
    x = np.linspace(0, year_number * 2 * np.pi, 365 * year_number)

    global_warming_func = x / global_warming_rate
    year_temp_change = temperature_change * np.sin(x) + global_warming_func + axial_shift
    decage_temp_change = np.sin(x / year_cycles / 2 / np.pi) / 10 + year_temp_change
    day_temp_change = (np.sin(365 * x) / 20 + year_temp_change)

    temp_prediction_func = (year_temp_change + decage_temp_change + day_temp_change) / 3

    plt.figure(figsize=(10, 6))
    plt.plot(x, temp_prediction_func, label='Прогноз 20 років уперед')
    plt.xlabel('x (день)')
    plt.ylabel('Температура')
    plt.title('Прогноз температури на 20 років уперед')
    plt.legend()
    plt.grid(True)
    plt.show()

predict_temperature()
