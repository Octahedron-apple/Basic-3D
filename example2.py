import functions
import numpy as np 
import math
from PIL import Image, ImageDraw
import os
import subprocess
directory_name = "Output"

try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created.")
except FileExistsError:
    p=0
except FileNotFoundError:
    print(f"Cannot create directory: a parent directory does not exist.")

obj=functions.unit_sphere(50)
for i in range(120):
    pro=functions.threeDtotwoD(obj,np.array([0,0,-100]),15)
    functions.draw_to_image(pro,f"Output/out-{i:03d}.png")
    obj=functions.rotate(obj,6,"X")
    obj=functions.rotate(obj,6,"Y")
subprocess.call(" ffmpeg -framerate 30 -i Output/out-%03d.png -c:v libx264 -pix_fmt yuv420p exp2.mp4 -y", shell=True)
