import tkinter as tk
from tkinter import filedialog
from tkinter import Tk, Canvas
import json
import numpy as np
from PIL import ImageGrab
import matplotlib.pyplot as plt

class PolynomialApproximationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Аппроксимация полиномом")

        # Создание элементов интерфейса
        self.degree_label = tk.Label(root, text="Степень полинома:")
        self.degree_label.pack()
        self.degree_entry = tk.Entry(root)
        self.degree_entry.pack()

        self.load_button = tk.Button(root, text="Загрузить данные", command=self.load_data)
        self.load_button.pack()

        self.approximate_button = tk.Button(root, text="Аппроксимировать", command=self.approximate)
        self.approximate_button.pack()

        self.error_label = tk.Label(root, text="Погрешность аппроксимации:")
        self.error_label.pack()

        self.save_button = tk.Button(root, text="Сохранить результаты", command=self.save_results)
        self.save_button.pack()

    def load_data(self):
        # Добавьте функционал загрузки данных из файла JSON
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Обработка данных
            self.x = data['x']
            self.y = data['y']

    def plot_results(self):
        # Создание нового окна для вывода графика
        plot_window = Tk()
        plot_window.title('График аппроксимации')

        canvas = Canvas(plot_window, width=800, height=600)  # Изменение размера окна
        canvas.pack()

        # Масштабирование координат точек для увеличения масштаба
        x_scale = 100  # масштаб по оси x
        y_scale = 50  # масштаб по оси y
        for i in range(len(self.x)):
            canvas.create_oval(self.x[i]*x_scale, self.y[i]*y_scale, self.x[i]*x_scale+5, self.y[i]*y_scale+5, fill='blue')

        for i in range(len(self.x)):
            y_fit = self.y_fit[i]*y_scale
            canvas.create_oval(self.x[i]*x_scale, y_fit, self.x[i]*x_scale+5, y_fit+5, fill='red')

        plot_window.mainloop()

    def approximate(self):
        # Реализуйте аппроксимацию экспериментальных данных полиномом выбранной степени
        degree = int(self.degree_entry.get())
        self.coefficients = np.polyfit(self.x, self.y, degree)

        # Вычисление полиномиальной аппроксимации
        self.y_fit = np.polyval(self.coefficients, self.x)

        # Вычисление погрешности аппроксимации
        self.error = np.mean((self.y - self.y_fit) ** 2)
        # Вычисление погрешности

        # Отображение погрешности на интерфейсе
        self.error_label.config(text="Погрешность аппроксимации: {}".format(self.error))

        # Построение графика
        self.plot_results()

    def save_results(self):
        # Сохранение коэффициентов, погрешностей и графиков в выбранные файлы
        filename = "results.png"

        # Создание нового окна для вывода графика
        plot_window = Tk()
        plot_window.title('График аппроксимации')

        canvas = Canvas(plot_window, width=800, height=600)  # Изменение размера окна
        canvas.pack()

        # Нанесение экспериментальных данных на график
        for i in range(len(self.x)):
            canvas.create_oval(self.x[i] * 50, self.y[i] * 50, self.x[i] * 50 + 5, self.y[i] * 50 + 5, fill='blue')

        # Нанесение аппроксимированных значений на график
        for i in range(len(self.x)):
            y_fit = self.y_fit[i] * 50
            canvas.create_oval(self.x[i] * 50, y_fit, self.x[i] * 50 + 5, y_fit + 5, fill='red')

        # Сохранение графика как изображения
        x0 = plot_window.winfo_rootx() + canvas.winfo_x()
        y0 = plot_window.winfo_rooty() + canvas.winfo_y()
        x1 = x0 + canvas.winfo_width()
        y1 = y0 + canvas.winfo_height()
        ImageGrab.grab().crop((x0, y0, x1, y1)).save(filename)

        plot_window.mainloop()
        save_data = {
            'coefficients': self.coefficients.tolist(),
            'error': self.error,
            'x': self.x,
            'y': self.y,
            'y_fit': self.y_fit.tolist()
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        with open(file_path, 'w') as file:
            json.dump(save_data, file)

root = tk.Tk()
app = PolynomialApproximationApp(root)
root.mainloop()