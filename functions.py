import numpy as np 
import math
def rotate(points, angle, axis):
    rad = math.radians(angle)
    c = math.cos(rad)
    s = math.sin(rad)
    if axis.upper() == 'X':
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ])
    elif axis.upper() == 'Y':
        rotation_matrix = np.array([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ])
    elif axis.upper() == 'Z':
        rotation_matrix = np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Axis must be 'X', 'Y', or 'Z'")

    rotated_points = []
    for point in points:
        
        rotated_point = np.dot(rotation_matrix, point)
        rotated_points.append(rotated_point)
    points=rotated_points
    return rotated_points
def translate(points, shift):
    tp = []
    for i in points:
        np = i + shift 
        tp.append(np)
    points=tp  
    return tp
def print_points(points):
    formatted_points = [f"({p[0]},{p[1]},{p[2]})" for p in points]
    print(",".join(formatted_points))
def unit_cube(scale):
    points = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
               
                point=np.array([x,y,z])*scale
                points.append(point)
                    
    return points
def unit_Sphere(scale):
    points = []
    for x in range(-2,3):
        for y in range(-2,3):
            for z in range(-2,3):
                vec = np.array([x, y, z])*0.5
                magnitude = np.linalg.norm(vec)
                unit_vec = vec / magnitude
                point = unit_vec * scale
                points.append(point)
def threeDtotwoD(points, camera, focal_length):
    relative=[]
    for i in range(len(points)):
        relative.append(points[i]-camera)
    return_points=[]
    for i in range(len(points)):
        return_points.append(np.array([focal_length*relative[i][0]/relative[i][2],focal_length*relative[i][1]/relative[i][2]]))
    return return_points
