import tkinter as tk
from tkinter import filedialog
import json
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных из файла JSON
def load_data():
    # Добавьте функционал загрузки данных из файла JSON
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    with open(file_path, 'r') as file:
        return json.load(file)

# Аппроксимация данных полиномом заданной степени
def polynomial_approximation(x, y, degree):
    coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)
    return polynomial

# Сохранение коэффициентов, погрешностей и графиков в файлы
def save_results(coefficients, errors, x, y, polynomial, file_path):
    results = {
        'coefficients': coefficients,
        'errors': errors,
        'x': x,
        'y': y,
        'polynomial': str(polynomial)
    }
    with open(file_path, 'w') as file:
        json.dump(results, file)

root = tk.Tk()
root.title("Аппроксимация полиномом")

# Создание элементов интерфейса
degree_label = tk.Label(root, text="Степень полинома:")
degree_label.pack()
degree_entry = tk.Entry(root)
degree_entry.pack()

load_button = tk.Button(root, text="Загрузить данные", command=load_data)
load_button.pack()

approximate_button = tk.Button(root, text="Аппроксимировать", command=approximate)
approximate_button.pack()

error_label = tk.Label(root, text="Погрешность аппроксимации:")
error_label.pack()

save_button = tk.Button(root, text="Сохранить результаты", command=save_results)
save_button.pack()

# Загрузка данных из файла JSON
data = load_data('data.json')

# Извлечение значений x и y из данных
x = data['x']
y = data['y']

# Выбор степени полинома
degree = 3

# Аппроксимация данных полиномом заданной степени
polynomial = polynomial_approximation(x, y, degree)

# Вычисление погрешности аппроксимации
approximated_y = polynomial(x)
errors = y - approximated_y

# Вывод графика с аппроксимацией и погрешностью
plt.scatter(x, y, label='Экспериментальные данные')
plt.plot(x, approximated_y, label='Аппроксимация')
plt.plot(x, errors, label='Погрешность')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

# Сохранение результатов в файл
save_results(polynomial.coefficients, errors, x, y, polynomial, 'results.json')