import argparse
import pygame
import sys
import numpy as np
from functions import Obj, Camera
from controls import get_movement_input, get_rotation_input
from char import Char_to_Object

parser = argparse.ArgumentParser(description="Basic 3D Engine")
parser.add_argument("-s", "--string", type=str, help="String to render as 3D text")
args = parser.parse_args()

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Basic-3D Engine")

clock = pygame.time.Clock()
fps = 60

main_obj = Obj()

if args.string:
    text_string = args.string
    spacing = 150
    start_x = -((len(text_string) * spacing) / 2)
    
    for i, char in enumerate(text_string):
        char_converter = Char_to_Object(char)
        char_obj = char_converter.make_object(scale_factor=12)
        char_obj.Translate(np.array([start_x + (i * spacing), 0.0, 0.0]))
        
        vertex_offset = len(main_obj.Points)
        main_obj.Points.extend(char_obj.Points)
        for face in char_obj.Faces:
            main_obj.Faces.append((face[0]+vertex_offset, face[1]+vertex_offset, face[2]+vertex_offset))
else:
    main_obj.Generate_Unit_Sphere(scale_factor=200)

camera = Camera(np.array([0.0, 0.0, -1000.0 if args.string else -600.0]))
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
    
    move_speed = 20.0 if args.string else 10.0
    camera.Translate(np.array([dx * move_speed, dy * move_speed, dz * move_speed]))
    
    if rx != 0:
        camera.Rotate(rx * 2.0, 1)
    if ry != 0:
        camera.Rotate(ry * 2.0, 0)

    screen.fill((20, 20, 30) if args.string else (0, 0, 0))

    if not args.string:
        main_obj.Rotate(1.5, 1)
        main_obj.Rotate(0.5, 0)

    projected = main_obj.Project_3D_To_2D(camera, focal_length)

    face_depths = []
    for face in main_obj.Faces:
        z0 = projected.Points[face[0]].Coordinates[2]
        z1 = projected.Points[face[1]].Coordinates[2]
        z2 = projected.Points[face[2]].Coordinates[2]
        avg_z = (z0 + z1 + z2) / 3.0
        
        if z0 > 0.1 and z1 > 0.1 and z2 > 0.1:
            face_depths.append((avg_z, face))
    
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
        
        if args.string:
            pygame.draw.polygon(screen, (0, 150, 255), pts)
        else:
            pygame.draw.polygon(screen, (0, 100, 200), pts)
            pygame.draw.polygon(screen, (255, 255, 255), pts, 1)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()
