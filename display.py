import sys
import json
import pygame
import numpy as np
from functions import Obj, Camera, Point
from controls import get_movement_input, get_rotation_input

def load_json_obj(filepath, scale=150.0):
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    obj = Obj()
    obj.Points = [Point(np.array([p[0] * scale, -p[1] * scale, p[2] * scale])) for p in data["points"]]
    obj.Faces = data["faces"]
    return obj

def main():
    
        
    json_filepath = sys.argv[1]
    
    print(f"Loading {json_filepath}...")
    target_obj = load_json_obj(json_filepath)
    print(f"Loaded object with {len(target_obj.Points)} points and {len(target_obj.Faces)} faces.")

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption(f"Basic-3D Engine - {json_filepath}")

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

        target_obj.Rotate(1.5, 1)

        projected = target_obj.Project_3D_To_2D(camera, focal_length)

        face_depths = []
        for face in target_obj.Faces:
            try:
                z0 = projected.Points[face[0]].Coordinates[2]
                z1 = projected.Points[face[1]].Coordinates[2]
                z2 = projected.Points[face[2]].Coordinates[2]
                avg_z = (z0 + z1 + z2) / 3.0
                
                if z0 > 0.1 and z1 > 0.1 and z2 > 0.1:
                    face_depths.append((avg_z, face))
            except IndexError:
                continue
        
        face_depths.sort(key=lambda x: x[0], reverse=True)
        sorted_faces = [f[1] for f in face_depths]

        for face in sorted_faces:
            p1 = projected.Points[face[0]].Coordinates
            p2 = projected.Points[face[1]].Coordinates
            p3 = projected.Points[face[2]].Coordinates
            
            pts = [
                (int(width / 2 + p1[0]), int(height / 2 + p1[1])),
                (int(width / 2 + p2[0]), int(height / 2 + p2[1])),
                (int(width / 2 + p3[0]), int(height / 2 + p3[1]))
            ]
            
            pygame.draw.polygon(screen, (0, 150, 255), pts)
            pygame.draw.polygon(screen, (255, 255, 255), pts, 1)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
