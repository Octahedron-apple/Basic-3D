import numpy as np 
import math
from PIL import Image, ImageDraw
import os
import subprocess
import pygame


class Point:
    def __init__(self, Coordinates, Radius=None):
        self.Coordinates = Coordinates
        self.Radius = Radius
        
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
            projected_obj.Points.append(Point(projected_coords, Radius=point.Radius))
            
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

    def Populate_Edges_From_Faces(self):
        edges_set = set()
        for face in self.Faces:
            n = len(face)
            for i in range(n):
                edge = tuple(sorted((face[i], face[(i + 1) % n])))
                edges_set.add(edge)
        self.Edges = list(edges_set)
        return self

    def Generate_Impostor_Grid(self, scale_factor=300, grid_size=3):
        self.Points = []
        self.Edges = []
        self.Faces = []
        
        if grid_size > 1:
            steps = np.linspace(-0.5, 0.5, grid_size)
        else:
            steps = [0.0]
            
        for x in steps:
            for y in steps:
                for z in steps:
                    point_coords = np.array([x, y, z]) * scale_factor
                    self.Points.append(Point(point_coords, Radius=20.0))
        return self

    def Generate_Single_Node(self, radius=150.0):
        self.Points = [Point(np.array([0.0, 0.0, 0.0]), Radius=radius)]
        self.Edges = []
        self.Faces = []
        return self


def draw_impostor_sphere(surface, center, radius, color):
    cx, cy = center
    r = int(radius)
    if r <= 0:
        return
    
    if r <= 3:
        pygame.draw.circle(surface, color, (int(cx), int(cy)), max(1, r))
        return
        
    base_r, base_g, base_b = color
    steps = max(3, min(r, 15))
    
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0.0
        factor = t * t
        
        curr_r = int(base_r + (255 - base_r) * factor * 0.85)
        curr_g = int(base_g + (255 - base_g) * factor * 0.85)
        curr_b = int(base_b + (255 - base_b) * factor * 0.85)
        
        curr_color = (
            max(0, min(255, curr_r)),
            max(0, min(255, curr_g)),
            max(0, min(255, curr_b))
        )
        
        curr_radius = int(r * (1.0 - t * 0.95))
        if curr_radius <= 0:
            curr_radius = 1
            
        offset_x = int(cx - t * r * 0.3)
        offset_y = int(cy - t * r * 0.3)
        
        pygame.draw.circle(surface, curr_color, (offset_x, offset_y), curr_radius)


def render_scene(screen, width, height, camera, focal_length, objects_with_colors, render_config, theme):
    # Allow passing a single object instead of a list
    if not isinstance(objects_with_colors, list):
        objects_with_colors = [(objects_with_colors, None)]
    elif len(objects_with_colors) > 0 and not isinstance(objects_with_colors[0], tuple):
        objects_with_colors = [(o, None) for o in objects_with_colors]
        
    primitives = []
    
    for obj_idx, (obj, color_overrides) in enumerate(objects_with_colors):
        projected = obj.Project_3D_To_2D(camera, focal_length)
        
        theme_face = theme["face"]
        theme_line = theme["line"]
        theme_node = theme["node"]
        
        if color_overrides is not None:
            f_col = color_overrides[0] if color_overrides[0] is not None else theme_face
            l_col = color_overrides[1] if color_overrides[1] is not None else theme_line
            n_col = color_overrides[2] if color_overrides[2] is not None else theme_node
        else:
            f_col, l_col, n_col = theme_face, theme_line, theme_node
            
        if render_config.get("faces", True):
            for face in obj.Faces:
                try:
                    z0 = projected.Points[face[0]].Coordinates[2]
                    z1 = projected.Points[face[1]].Coordinates[2]
                    z2 = projected.Points[face[2]].Coordinates[2]
                    
                    if z0 > 0.1 and z1 > 0.1 and z2 > 0.1:
                        avg_z = (z0 + z1 + z2) / 3.0
                        primitives.append((avg_z, 'face', face, projected, f_col, l_col))
                except IndexError:
                    continue
        
        elif render_config.get("lines", True):
            if not obj.Edges:
                obj.Populate_Edges_From_Faces()
                
            for edge in obj.Edges:
                try:
                    z0 = projected.Points[edge[0]].Coordinates[2]
                    z1 = projected.Points[edge[1]].Coordinates[2]
                    
                    if z0 > 0.1 and z1 > 0.1:
                        avg_z = (z0 + z1) / 2.0
                        primitives.append((avg_z, 'edge', edge, projected, l_col))
                except IndexError:
                    continue
                    
        if render_config.get("nodes", True):
            for i, p in enumerate(obj.Points):
                try:
                    z = projected.Points[i].Coordinates[2]
                    if z > 0.1:
                        r_3d = p.Radius if p.Radius is not None else render_config.get("default_node_radius", 6.0)
                        primitives.append((z, 'node', i, projected, n_col, r_3d))
                except IndexError:
                    continue

    primitives.sort(key=lambda x: x[0], reverse=True)
    
    for prim in primitives:
        prim_type = prim[1]
        
        if prim_type == 'face':
            _, _, face, proj, f_col, l_col = prim
            p1 = proj.Points[face[0]].Coordinates
            p2 = proj.Points[face[1]].Coordinates
            p3 = proj.Points[face[2]].Coordinates
            
            pts = [
                (int(width / 2 + p1[0]), int(height / 2 + p1[1])),
                (int(width / 2 + p2[0]), int(height / 2 + p2[1])),
                (int(width / 2 + p3[0]), int(height / 2 + p3[1]))
            ]
            
            if f_col is not False and f_col is not None:
                pygame.draw.polygon(screen, f_col, pts)
            if render_config.get("lines", True) and l_col is not False and l_col is not None:
                pygame.draw.polygon(screen, l_col, pts, 1)
                
        elif prim_type == 'edge':
            _, _, edge, proj, l_col = prim
            p1 = proj.Points[edge[0]].Coordinates
            p2 = proj.Points[edge[1]].Coordinates
            
            pt1 = (int(width / 2 + p1[0]), int(height / 2 + p1[1]))
            pt2 = (int(width / 2 + p2[0]), int(height / 2 + p2[1]))
            
            if l_col is not False and l_col is not None:
                pygame.draw.line(screen, l_col, pt1, pt2, 1)
            
        elif prim_type == 'node':
            depth, _, idx, proj, n_col, r_3d = prim
            p = proj.Points[idx].Coordinates
            center = (int(width / 2 + p[0]), int(height / 2 + p[1]))
            
            r_2d = int(r_3d * focal_length / depth)
            if r_2d < 1:
                r_2d = 1
                
            if n_col is not False and n_col is not None:
                if render_config.get("node_style", "dot") == "impostor":
                    draw_impostor_sphere(screen, center, r_2d, n_col)
                else:
                    pygame.draw.circle(screen, n_col, center, r_2d)


def load_json_obj(filepath, scale=150.0):
    import json
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    obj = Obj()
    obj.Points = [Point(np.array([p[0] * scale, -p[1] * scale, p[2] * scale])) for p in data["points"]]
    obj.Faces = [tuple(f) for f in data["faces"]]
    obj.Populate_Edges_From_Faces()
    return obj