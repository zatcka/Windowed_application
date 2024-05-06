from math import *
from tkinter import *

f = input('f(x):')

root = Tk()

canv = Canvas(root, width = 1000, height = 1000, bg = "lightblue", cursor = "pencil")
canv.create_line(500,1000,500,0,width=2,arrow=LAST)
canv.create_line(0,500,1000,500,width=2,arrow=LAST)

First_x = -500;

for i in range(16000):
	x = First_x + (1 / 16) * i
	new_f = f.replace('x', str(x))
	y = -eval(new_f) + 500
	x += 500
	canv.create_oval(x, y, x + 1, y + 1, fill = 'black')

canv.pack()
root.mainloop()