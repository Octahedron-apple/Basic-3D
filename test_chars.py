import pygame
import sys
import numpy as np
from functions import Obj, Camera, render_scene
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
    obj.Populate_Edges_From_Faces()
    all_objects.append(obj)

camera = Camera(np.array([0.0, 0.0, -1000.0]))
focal_length = 600

# Hand-crafted premium color themes
COLOR_THEMES = [
    {
        "name": "Neon Cyberpunk",
        "background": (10, 10, 20),
        "face": (40, 20, 80),
        "line": (0, 255, 240),
        "node": (255, 0, 128)
    },
    {
        "name": "Sunset Glow",
        "background": (30, 10, 20),
        "face": (120, 40, 60),
        "line": (255, 100, 50),
        "node": (255, 210, 100)
    },
    {
        "name": "Forest Mint",
        "background": (10, 25, 20),
        "face": (20, 60, 45),
        "line": (50, 200, 120),
        "node": (180, 255, 200)
    },
    {
        "name": "Lava / Inferno",
        "background": (15, 5, 5),
        "face": (80, 15, 10),
        "line": (255, 69, 0),
        "node": (255, 215, 0)
    },
    {
        "name": "Monochrome Slate",
        "background": (15, 17, 20),
        "face": (40, 44, 52),
        "line": (160, 172, 185),
        "node": (240, 244, 248)
    }
]

theme_idx = 0
active_theme = COLOR_THEMES[theme_idx]

# Render configuration defaults
render_config = {
    "faces": True,
    "lines": True,
    "nodes": True,
    "node_style": "dot",  # "dot" or "impostor"
    "default_node_radius": 6.0
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_c:
                theme_idx = (theme_idx + 1) % len(COLOR_THEMES)
                active_theme = COLOR_THEMES[theme_idx]
            elif event.key == pygame.K_n:
                render_config["nodes"] = not render_config["nodes"]
            elif event.key == pygame.K_l:
                render_config["lines"] = not render_config["lines"]
            elif event.key == pygame.K_f:
                render_config["faces"] = not render_config["faces"]
            elif event.key == pygame.K_i:
                render_config["node_style"] = "impostor" if render_config["node_style"] == "dot" else "dot"

    dx, dy, dz = get_movement_input()
    rx, ry = get_rotation_input()
    
    local_move = np.array([dx * 20.0, dy * 20.0, dz * 20.0])
    world_move = np.dot(camera.Orientation, local_move)
    camera.Translate(world_move)
    
    if rx != 0:
        camera.Rotate(rx * 2.0, 1)
    if ry != 0:
        camera.Rotate(ry * 2.0, 0)

    # Fill background based on active theme
    screen.fill(active_theme["background"])

    # Render scene using our unified rendering pipeline
    render_scene(screen, width, height, camera, focal_length, all_objects, render_config, active_theme)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()
