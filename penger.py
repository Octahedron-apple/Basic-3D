import sys
import json
import pygame
import numpy as np
from functions import Obj, Camera, Point
from controls import get_movement_input, get_rotation_input
from char import Char_to_Object

def load_json_obj(filepath, scale=150.0):
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    obj = Obj()
    obj.Points = [Point(np.array([p[0] * scale, -p[1] * scale, p[2] * scale])) for p in data["points"]]
    obj.Faces = data["faces"]
    return obj

def create_text_obj(text_string, scale_factor=12, spacing=150):
    text_obj = Obj()
    start_x = -((len(text_string) * spacing) / 2)
    
    for i, char in enumerate(text_string):
        char_converter = Char_to_Object(char)
        char_obj = char_converter.make_object(scale_factor=scale_factor)
        char_obj.Translate(np.array([start_x + (i * spacing), 0.0, 0.0]))
        
        vertex_offset = len(text_obj.Points)
        text_obj.Points.extend(char_obj.Points)
        for face in char_obj.Faces:
            text_obj.Faces.append((face[0]+vertex_offset, face[1]+vertex_offset, face[2]+vertex_offset))
            
    return text_obj

def main():
    json_filepath = "penger.json"
    
    print(f"Loading {json_filepath}...")
    penger_obj = load_json_obj(json_filepath)
    penger_obj.Scale(2)
    text_obj = create_text_obj("PENGER")
    text_obj.Translate(np.array([75.0, 300.0, 0.0]))

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption(f"Basic-3D Engine - Penger")

    clock = pygame.time.Clock()
    fps = 60

    camera = Camera(np.array([0.0, 0.0, -1000.0]))
    focal_length = 600

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        dx, dy, dz = get_movement_input()
        rx, ry = get_rotation_input()
        
        move_speed = 20.0
        camera.Translate(np.array([dx * move_speed, dy * move_speed, dz * move_speed]))
        
        if rx != 0:
            camera.Rotate(rx * 2.0, 1)
        if ry != 0:
            camera.Rotate(ry * 2.0, 0)

        screen.fill((20, 20, 30))

        penger_obj.Rotate(1.5, 1)

        projected_penger = penger_obj.Project_3D_To_2D(camera, focal_length)
        projected_text = text_obj.Project_3D_To_2D(camera, focal_length)

        face_depths = []
        
        for face in penger_obj.Faces:
            try:
                z0 = projected_penger.Points[face[0]].Coordinates[2]
                z1 = projected_penger.Points[face[1]].Coordinates[2]
                z2 = projected_penger.Points[face[2]].Coordinates[2]
                avg_z = (z0 + z1 + z2) / 3.0
                
                if z0 > 0.1 and z1 > 0.1 and z2 > 0.1:
                    face_depths.append((avg_z, face, projected_penger, (0, 100, 200), True))
            except IndexError:
                continue
                
        for face in text_obj.Faces:
            try:
                z0 = projected_text.Points[face[0]].Coordinates[2]
                z1 = projected_text.Points[face[1]].Coordinates[2]
                z2 = projected_text.Points[face[2]].Coordinates[2]
                avg_z = (z0 + z1 + z2) / 3.0
                
                if z0 > 0.1 and z1 > 0.1 and z2 > 0.1:
                    face_depths.append((avg_z, face, projected_text, (0, 150, 255), False))
            except IndexError:
                continue
        
        face_depths.sort(key=lambda x: x[0], reverse=True)

        for depth, face, proj, color, draw_lines in face_depths:
            p1 = proj.Points[face[0]].Coordinates
            p2 = proj.Points[face[1]].Coordinates
            p3 = proj.Points[face[2]].Coordinates
            
            pts = [
                (int(width / 2 + p1[0]), int(height / 2 + p1[1])),
                (int(width / 2 + p2[0]), int(height / 2 + p2[1])),
                (int(width / 2 + p3[0]), int(height / 2 + p3[1]))
            ]
            
            pygame.draw.polygon(screen, color, pts)
            if draw_lines:
                pygame.draw.polygon(screen, (255, 255, 255), pts, 1)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
