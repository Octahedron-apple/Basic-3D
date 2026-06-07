import numpy as np 
import math
from PIL import Image, ImageDraw
import os
import subprocess

class Point:
    def __init__(self, Coordinates):
        self.coords = Coordinates
    def rotate(self, angle, axis):
         

       
class Obj:
    def __init__(self, points=None):
        if points is None:
            self.points = []
        else:
            self.points = points

    def rotate(self, angle, axis):
        angle_radians = math.radians(angle)
        cos_val = math.cos(angle_radians)
        sin_val = math.sin(angle_radians)
        
        if axis.upper() == 'X':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, cos_val, -sin_val],
                [0, sin_val, cos_val]
            ])
        elif axis.upper() == 'Y':
            rotation_matrix = np.array([
                [cos_val, 0, sin_val],
                [0, 1, 0],
                [-sin_val, 0, cos_val]
            ])
        elif axis.upper() == 'Z':
            rotation_matrix = np.array([
                [cos_val, -sin_val, 0],
                [sin_val, cos_val, 0],
                [0, 0, 1]
            ])
        else:
            raise ValueError("Axis must be 'X', 'Y', or 'Z'")

        result_points = []
        for point in self.points:
            coords = point.coords if hasattr(point, 'coords') else point
            new_coords = np.dot(rotation_matrix, coords)
            result_points.append(Point(new_coords))
        self.points = result_points
        return self

    def translate(self, shift_vector):
        translated_points = []
        for point in self.points:
            coords = point.coords if hasattr(point, 'coords') else point
            new_coords = coords + shift_vector 
            translated_points.append(Point(new_coords))
        self.points = translated_points
        return self

    def print_points(self):
        formatted_strings = [f"({point[0]},{point[1]},{point[2]})" for point in self.points]
        print(",".join(formatted_strings))

    def generate_unit_cube(self, scale_factor):
        self.points = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    point_coords = np.array([x, y, z]) * scale_factor
                    self.points.append(Point(point_coords))
        return self

    def generate_unit_sphere(self, scale_factor):
        self.points = []
        for x in range(-2, 3):
            for y in range(-2, 3):
                for z in range(-2, 3):
                    vector = np.array([x, y, z]) * 0.5
                    magnitude = np.linalg.norm(vector)
                    if magnitude == 0:
                        continue
                    unit_vector = vector / magnitude
                    point_coords = unit_vector * scale_factor
                    self.points.append(Point(point_coords))
        return self

    def generate_unit_cone(self, scale_factor):
        self.points = []
        for i in range(11):
            height = i / 10.0
            radius = 1.0 - height
            for j in range(21):
                angle = j * (math.pi * 2 / 20.0)
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                point_coords = np.array([x, y, height - 0.5]) * scale_factor
                self.points.append(Point(point_coords))
        return self

    def project_3d_to_2d(self, camera_position, focal_length): 
        relative_points = []
        for point in self.points:
            coords = point.coords if hasattr(point, 'coords') else point
            relative_points.append(coords - camera_position)
            
        projected_points = []
        for rel_point in relative_points:
            z = rel_point[2]
            if z == 0: 
                z = 0.001
            projected_points.append(Point([focal_length * rel_point[0] / z, focal_length * rel_point[1] / z]))
        
        return Obj(projected_points)

    def draw_to_image(self, filename="Out.png"):
        image = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(image)
        center_x, center_y = 250, 250
        
        for point in self.points:
            x = point[0]
            y = point[1]
            screen_x = center_x + x
            screen_y = center_y + y
            radius = 2
            draw.ellipse(
                (screen_x - radius, screen_y - radius, screen_x + radius, screen_y + radius), 
                fill='black'
            )
        image.save(filename)

    def print_points_2d(self):
        formatted_strings = [f"({point[0]},{point[1]})" for point in self.points]
        print(",".join(formatted_strings))

    def generate_unit_circle(self, scale_factor, axis):
        if axis.upper() == 'X':
            start_point = [0, 0, scale_factor]
        elif axis.upper() == 'Y':
            start_point = [0, 0, scale_factor]
        elif axis.upper() == 'Z':
            start_point = [0, scale_factor, 0]
        else:
            raise ValueError("Axis must be 'X', 'Y', or 'Z'")
        
        temp_obj = Obj([Point(start_point)])
        self.points = []
        for _ in range(20):
            temp_obj.rotate(18, axis)
            self.points.append(Point(temp_obj.points[0].coords))
        return self

    def stretch(self, axis, scale_factor):
        result_points = []
        for point in self.points:
            coords = point.coords if hasattr(point, 'coords') else point
            x, y, z = coords[0], coords[1], coords[2]
            
            if axis.upper() == 'X': 
                x *= scale_factor
            elif axis.upper() == 'Y': 
                y *= scale_factor
            elif axis.upper() == 'Z': 
                z *= scale_factor
            else: 
                raise ValueError("Axis must be 'X', 'Y', or 'Z'")
                
            result_points.append(Point([x, y, z]))
        self.points = result_points
        return self

    def scale(self, scale_factor):
        result_points = []
        for point in self.points:
            coords = point.coords if hasattr(point, 'coords') else point
            new_coords = coords * scale_factor
            result_points.append(Point(new_coords))
        self.points = result_points
        return self
