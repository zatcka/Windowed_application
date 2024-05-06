import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import matplotlib matplotlib.use("TkAgg")
import json
import os
import datetime


def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def approximate():
    degree = int(degree_entry.get())
    file_path = file_path_label.cget("text").split(": ")[1]
    data = load_data_from_json(file_path)
    x = np.array(data['x'])
    y = np.array(data['y'])
    coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)
    plt.clf()
    plt.scatter(x, y, label='Входные данный')
    x_range = np.linspace(min(x), max(x), 100)
    plt.plot(x_range, polynomial(x_range), label='Аппроксимация')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.savefig('graph.png')
    #plt.draw()
    approximated_y = polynomial(x)
    error = np.mean(np.abs(approximated_y - y))
    coefficients_label.config(text='Коэффициенты: {}'.format(coefficients))
    error_label.config(text='Погрешность: {}'.format(error))
    plt.show()
    # y_fit = poly(x)
    # plt.plot(x, y_fit, label=f'Аппроксимация с полиномом {degree} степени')
    # canvas = FigureCanvasTkAgg(fig,master=root)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    file_path_label.config(text='Selected file: {}'.format(file_path))

def save():
    file_path = filedialog.askdirectory()
    coefficients = coefficients_label.cget("text").split(": ")[1]
    errors = error_label.cget("text").split(": ")[1]
    # using now() to get current time
    current_time = datetime.datetime.now()
    time = str(current_time).replace(':', '.')
    with open(file_path + '/results ' + time + '.txt', 'w') as file:
        file.write('Coefficients: {}\n'.format(coefficients))
        file.write('Errors: {}\n'.format(errors))
        # Move a file by renaming it's path
        os.rename('graph.png', file_path + '/Graph ' + time + '.png')


# Создание главного окна
window = tk.Tk()
window.title('Аппроксимация данных')
window.geometry('400x250')

# Создание элементов управления
file_path_label = tk.Label(window, text='Выбранный путь: ')
file_path_label.pack()

file_select_button = tk.Button(window, text='Выбрать файл', command=select_file)
file_select_button.pack()

degree_label = tk.Label(window, text='Степень полинома:')
degree_label.pack()

degree_entry = tk.Entry(window)
degree_entry.pack()

approximate_button = tk.Button(window, text='Аппроксимировать', command=approximate)
approximate_button.pack()

coefficients_label = tk.Label(window, text='Коэффициенты:')
coefficients_label.pack()

error_label = tk.Label(window, text='Погрешность: ')
error_label.pack()

save_button = tk.Button(window, text='Сохранить', command=save)
save_button.pack()

# Запуск главного цикла обработки событий
window.mainloop()