import numpy as np 
import math
from PIL import Image, ImageDraw
import os
import subprocess

class Point:
    def __init__(self, Coordinates):
        self.Coordinates = Coordinates
        
    def Rotate(self, angle, axis):
        # Axis Can be either of 0,1,2 (X,Y,Z)
        angle_radians = math.radians(angle)
        cos_val = math.cos(angle_radians)
        sin_val = math.sin(angle_radians)
        
        if axis == 0:
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, cos_val, -sin_val],
                [0, sin_val, cos_val]
            ])
        elif axis == 1:
            rotation_matrix = np.array([
                [cos_val, 0, sin_val],
                [0, 1, 0],
                [-sin_val, 0, cos_val]
            ])
        elif axis == 2:
            rotation_matrix = np.array([
                [cos_val, -sin_val, 0],
                [sin_val, cos_val, 0],
                [0, 0, 1]
            ])
        else:
            raise ValueError("Axis must be 0, 1, or 2 (X, Y, or Z)")

        self.Coordinates = np.dot(rotation_matrix, self.Coordinates)
        return self

    def Translate(self, shift_vector):
        self.Coordinates = self.Coordinates + shift_vector
        return self

    def Stretch(self, axis, scale_factor):
        if axis in (0, 1, 2):
            self.Coordinates[axis] *= scale_factor
        else:
            raise ValueError("Axis must be 0, 1, or 2")
        return self

    def Scale(self, scale_factor):
        self.Coordinates = self.Coordinates * scale_factor
        return self

class Obj:
    def __init__(self):
        self.Points = []

    def Rotate(self, angle, axis):
        for point in self.Points:
            point.Rotate(angle, axis)
        return self

    def Translate(self, shift_vector):
        for point in self.Points:
            point.Translate(shift_vector)
        return self

    def Stretch(self, axis, scale_factor):
        for point in self.Points:
            point.Stretch(axis, scale_factor)
        return self

    def Scale(self, scale_factor):
        for point in self.Points:
            point.Scale(scale_factor)
        return self

    def Print_Points(self):
        formatted_strings = [f"({point.Coordinates[0]},{point.Coordinates[1]},{point.Coordinates[2]})" for point in self.Points]
        print(",".join(formatted_strings))

    def Print_Points_2D(self):
        formatted_strings = [f"({point.Coordinates[0]},{point.Coordinates[1]})" for point in self.Points]
        print(",".join(formatted_strings))

    def Generate_Unit_Cube(self, scale_factor):
        self.Points = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    point_coords = np.array([x, y, z]) * scale_factor
                    self.Points.append(Point(point_coords))
        return self

    def Generate_Unit_Sphere(self, scale_factor):
        self.Points = []
        for x in range(-2, 3):
            for y in range(-2, 3):
                for z in range(-2, 3):
                    vector = np.array([x, y, z]) * 0.5
                    magnitude = np.linalg.norm(vector)
                    if magnitude == 0:
                        continue
                    unit_vector = vector / magnitude
                    point_coords = unit_vector * scale_factor
                    self.Points.append(Point(point_coords))
        return self

    def Generate_Unit_Cone(self, scale_factor):
        self.Points = []
        for i in range(11):
            height = i / 10.0
            radius = 1.0 - height
            for j in range(21):
                angle = j * (math.pi * 2 / 20.0)
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                point_coords = np.array([x, y, height - 0.5]) * scale_factor
                self.Points.append(Point(point_coords))
        return self

    def Generate_Unit_Circle(self, scale_factor, axis):
        if axis == 0:
            start_point = np.array([0, 0, scale_factor])
        elif axis == 1:
            start_point = np.array([0, 0, scale_factor])
        elif axis == 2:
            start_point = np.array([0, scale_factor, 0])
        else:
            raise ValueError("Axis must be 0, 1, or 2")
        
        self.Points = []
        temp_point = Point(start_point)
        for _ in range(20):
            temp_point.Rotate(18, axis)
            self.Points.append(Point(temp_point.Coordinates.copy()))
        return self

    def Project_3D_To_2D(self, camera_position, focal_length): 
        projected_obj = Obj()
        for point in self.Points:
            rel_point = point.Coordinates - camera_position
            z = rel_point[2]
            if z == 0: 
                z = 0.001
            projected_coords = np.array([focal_length * rel_point[0] / z, focal_length * rel_point[1] / z])
            projected_obj.Points.append(Point(projected_coords))
        return projected_obj

    def Draw_To_Image(self, filename="Out.png"):
        image = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(image)
        center_x, center_y = 250, 250
        
        for point in self.Points:
            x = point.Coordinates[0]
            y = point.Coordinates[1]
            screen_x = center_x + x
            screen_y = center_y + y
            radius = 2
            draw.ellipse(
                (screen_x - radius, screen_y - radius, screen_x + radius, screen_y + radius), 
                fill='black'
            )
        image.save(filename)