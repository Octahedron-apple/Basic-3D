import tkinter as tk 
import functions
import numpy as np 
import time

def dp(x, y, r=2, c="black"):
    x1, y1 = x - r, y - r
    x2, y2 = x + r, y + r
    cv.create_oval(x1, y1, x2, y2, fill=c, outline=c)

ob = functions.unit_cone(50)
rt = tk.Tk()

rt.geometry("500x500")
rt.title("3D animation - Cone")
cv = tk.Canvas(rt, width=500, height=500, bg="white")
cv.pack()

while True:
    cv.delete("all")
    pr = functions.threeDtotwoD(ob, np.array([0, 0, -100]), 15)
    for i in pr:
        # Scale and center on screen
        dp(i[0]*4 + 250, i[1]*4 + 250, 2, "red")
    
    # Rotate for animation
    ob = functions.rotate(ob, 5, "X")
    ob = functions.rotate(ob, 3, "Y")
    
    try:
        rt.update() 
        rt.update_idletasks()
    except:
        break
    time.sleep(0.02)
