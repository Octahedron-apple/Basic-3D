import numpy as np 
import math
from PIL import Image, ImageDraw
import os
import subprocess

class Point:
    def __init__(self, Coordinates):
        self.Coordinates = Coordinates
        
    def Rotate(self, angle, axis):
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

class Camera:
    def __init__(self, position):
        self.Coordinates = position
        self.Orientation = np.eye(3)
        
    def Translate(self, shift_vector):
        self.Coordinates = self.Coordinates + shift_vector
        return self
        
    def Rotate(self, angle, axis):
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

        self.Orientation = np.dot(rotation_matrix, self.Orientation)
        return self

class Obj:
    def __init__(self):
        self.Points = []
        self.Edges = []
        self.Faces = []

    def Remove_Duplicate_Points(self, tolerance=1e-5):
        unique_points = []
        for point in self.Points:
            is_duplicate = False
            for u_point in unique_points:
                if np.linalg.norm(point.Coordinates - u_point.Coordinates) < tolerance:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_points.append(point)
        self.Points = unique_points
        return self

    def Auto_Triangulate(self):
        self.Edges = set()
        self.Faces = set()
        n = len(self.Points)
        
        closest_neighbors = {}
        for i in range(n):
            distances = []
            for j in range(n):
                if i != j:
                    dist = np.linalg.norm(self.Points[i].Coordinates - self.Points[j].Coordinates)
                    distances.append((dist, j))
            distances.sort(key=lambda x: x[0])
            top_3 = [idx for d, idx in distances[:3]]
            closest_neighbors[i] = top_3
            
            for j in top_3:
                edge = tuple(sorted((i, j)))
                self.Edges.add(edge)
                
        for i in range(n):
            neighbors = closest_neighbors[i]
            for idx1 in range(len(neighbors)):
                for idx2 in range(idx1 + 1, len(neighbors)):
                    j = neighbors[idx1]
                    k = neighbors[idx2]
                    edge_jk = tuple(sorted((j, k)))
                    if edge_jk in self.Edges:
                        face = tuple(sorted((i, j, k)))
                        self.Faces.add(face)
                        
        self.Edges = list(self.Edges)
        self.Faces = list(self.Faces)
        return self

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

    def Generate_Unit_Sphere(self, scale_factor, lat_count=12, lon_count=24):
        self.Points = []
        self.Edges = []
        self.Faces = []
        
        for lat_num in range(lat_count + 1):
            theta = lat_num * math.pi / lat_count 
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            
            for lon_num in range(lon_count):
                phi = lon_num * 2 * math.pi / lon_count 
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)
                
                x = cos_phi * sin_theta
                y = sin_phi * sin_theta
                z = cos_theta
                
                self.Points.append(Point(np.array([x, y, z]) * scale_factor))
                
        for lat_num in range(lat_count):
            for lon_num in range(lon_count):
                first = (lat_num * lon_count) + lon_num
                second = first + lon_count
                
                next_lon = (lon_num + 1) % lon_count
                
                first_next = (lat_num * lon_count) + next_lon
                second_next = ((lat_num + 1) * lon_count) + next_lon
                
                self.Faces.append((first, second, first_next))
                self.Faces.append((second, second_next, first_next))
                
                self.Edges.append((first, second))
                self.Edges.append((first, first_next))
                
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

    def Project_3D_To_2D(self, camera, focal_length): 
        projected_obj = Obj()
        projected_obj.Edges = self.Edges.copy()
        projected_obj.Faces = self.Faces.copy()
        
        inv_orientation = camera.Orientation.T
        
        for point in self.Points:
            rel_point = point.Coordinates - camera.Coordinates
            aligned_point = np.dot(inv_orientation, rel_point)
            
            z = aligned_point[2]
            if z == 0: 
                z = 0.001
                
            projected_coords = np.array([
                focal_length * aligned_point[0] / z, 
                focal_length * aligned_point[1] / z,
                z
            ])
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