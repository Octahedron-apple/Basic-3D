import pygame
import sys
import numpy as np
from functions import Obj, Camera
from char import Char_to_Object
from controls import get_movement_input, get_rotation_input

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("3D Font Test")

clock = pygame.time.Clock()
fps = 60

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?"
all_objects = []

spacing = 150 
start_x = -((len(characters) * spacing) / 2)

for i, char in enumerate(characters):
    char_converter = Char_to_Object(char)
    obj = char_converter.make_object(scale_factor=12)
    
    obj.Translate(np.array([start_x + (i * spacing), 0.0, 0.0]))
    all_objects.append(obj)

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
    
    camera.Translate(np.array([dx * 20.0, dy * 20.0, dz * 20.0]))
    
    if rx != 0:
        camera.Rotate(rx * 2.0, 1)
    if ry != 0:
        camera.Rotate(ry * 2.0, 0)

    screen.fill((20, 20, 30))

    all_face_depths = []

    for obj in all_objects:
        projected = obj.Project_3D_To_2D(camera, focal_length)

        for face in obj.Faces:
            z0 = projected.Points[face[0]].Coordinates[2]
            z1 = projected.Points[face[1]].Coordinates[2]
            z2 = projected.Points[face[2]].Coordinates[2]
            avg_z = (z0 + z1 + z2) / 3.0
            
            if z0 > 0.1 and z1 > 0.1 and z2 > 0.1:
                p1 = projected.Points[face[0]].Coordinates
                p2 = projected.Points[face[1]].Coordinates
                p3 = projected.Points[face[2]].Coordinates
                all_face_depths.append((avg_z, p1, p2, p3))
    
    all_face_depths.sort(key=lambda x: x[0], reverse=True)

    for depth, p1, p2, p3 in all_face_depths:
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
