import pygame
import sys
import numpy as np
from functions import Obj

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Spinning Solid Sphere")

clock = pygame.time.Clock()
fps = 60

sphere = Obj().Generate_Unit_Sphere(scale_factor=200)

camera_position = np.array([0, 0, -600])
focal_length = 600

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((0, 0, 0))

    sphere.Rotate(1.5, 1)
    sphere.Rotate(0.5, 0)

    face_depths = []
    for face in sphere.Faces:
        z0 = sphere.Points[face[0]].Coordinates[2]
        z1 = sphere.Points[face[1]].Coordinates[2]
        z2 = sphere.Points[face[2]].Coordinates[2]
        avg_z = (z0 + z1 + z2) / 3.0
        face_depths.append((avg_z, face))
    
    face_depths.sort(key=lambda x: x[0], reverse=True)
    sorted_faces = [f[1] for f in face_depths]

    projected = sphere.Project_3D_To_2D(camera_position, focal_length)

    for face in sorted_faces:
        p1 = projected.Points[face[0]].Coordinates
        p2 = projected.Points[face[1]].Coordinates
        p3 = projected.Points[face[2]].Coordinates
        
        pts = [
            (int(width / 2 + p1[0]), int(height / 2 + p1[1])),
            (int(width / 2 + p2[0]), int(height / 2 + p2[1])),
            (int(width / 2 + p3[0]), int(height / 2 + p3[1]))
        ]
        
        pygame.draw.polygon(screen, (0, 100, 200), pts)
        
        pygame.draw.polygon(screen, (255, 255, 255), pts, 1)

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
sys.exit()
