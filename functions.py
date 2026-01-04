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
