import numpy as np 
import math
from PIL import Image, ImageDraw
import os
import subprocess

def rotate(ps, a, ax):
    rd = math.radians(a)
    c = math.cos(rd)
    s = math.sin(rd)
    if ax.upper() == 'X':
        m = np.array([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ])
    elif ax.upper() == 'Y':
        m = np.array([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ])
    elif ax.upper() == 'Z':
        m = np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Axis must be 'X', 'Y', or 'Z'")

    rp = []
    for p in ps:
        np_ = np.dot(m, p)
        rp.append(np_)
    return rp

def translate(ps, s):
    tp = []
    for p in ps:
        np_ = p + s 
        tp.append(np_)
    return tp

def print_points(ps):
    fs = [f"({p[0]},{p[1]},{p[2]})" for p in ps]
    print(",".join(fs))

def unit_cube(s):
    ps = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                p=np.array([x,y,z])*s
                ps.append(p)
    return ps

def unit_Sphere(s):
    ps = []
    for x in range(-2,3):
        for y in range(-2,3):
            for z in range(-2,3):
                v = np.array([x, y, z])*0.5
                m = np.linalg.norm(v)
                if m == 0:
                    continue
                uv = v / m
                p = uv * s
                ps.append(p)
    return ps

def unit_cone(s):
    ps = []
    for i in range(11):
        h = i / 10.0
        r = 1.0 - h
        for j in range(21):
            a = j * (math.pi * 2 / 20.0)
            x = r * math.cos(a)
            y = r * math.sin(a)
            p = np.array([x, y, h - 0.5]) * s
            ps.append(p)
    return ps

def threeDtotwoD(ps, c, f): 
    rl=[]
    for i in range(len(ps)):
        rl.append(ps[i]-c)
    rp=[]
    for i in range(len(ps)):
        z = rl[i][2]
        if z == 0: z = 0.001
        rp.append(np.array([f*rl[i][0]/z,f*rl[i][1]/z]))
    return rp

def draw_to_image(ps, fn="Out.png"):
    im = Image.new('RGB', (500, 500), 'white')
    dw = ImageDraw.Draw(im)
    cx, cy = 250, 250
    for p in ps:
        x=p[0]
        y=p[1]
        sx = cx + x
        sy = cy + y
        r = 2
        dw.ellipse(
            (sx - r, sy - r, sx + r, sy + r), 
            fill='black'
        )
    im.save(fn)

def print_points_2D(ps):
    fs = [f"({p[0]},{p[1]})" for p in ps]
    print(",".join(fs))

def unit_circle(s, ax):
    if ax.upper() == 'X':
        a = [0,0,s]
    elif ax.upper() == 'Y':
        a = [0,0,s]
    elif ax.upper() == 'Z':
        a = [0,s,0]
    else:
        raise ValueError("Axis must be 'X', 'Y', or 'Z'")
    ps =[]
    for i in range(20):
        ps.append(rotate(a,18,ax))
    return ps

def strech(ps, ax, s):
    rp = []
    for p in ps:
        x, y, z = p[0], p[1], p[2]
        if ax.upper() == 'X': x *= s
        elif ax.upper() == 'Y': y *= s
        elif ax.upper() == 'Z': z *= s
        else: raise ValueError("Axis must be 'X', 'Y', or 'Z'")
        rp.append(np.array([x, y, z]))
    return rp

def scale(ps, s):
    rp = []
    for p in ps:
        np_ = p * s
        rp.append(np_)
    return rp
