import tkinter as tk 
import functions
import numpy as np 
import time
def draw_point(x, y, radius=2, color="black"):
    x1 = x - radius
    y1 = y - radius
    x2 = x + radius
    y2 = y + radius
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
obj=functions.unit_cube(50)
root=tk.Tk()

root.geometry("500x500")
root.title("3D animation")
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()
while True:
    canvas.delete("all")
    pro=functions.threeDtotwoD(obj,np.array([0,0,-100]),15)
    for i in pro:
        draw_point(i[0]+250,i[1]+250,2)
    obj=functions.rotate(obj,6,"X")
    obj=functions.rotate(obj,6,"Y")
    try:
        root.update() 
        root.update_idletasks()
    except tk.TclError:
        break
    time.sleep(0.02)
