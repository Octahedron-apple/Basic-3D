import argparse
import pygame
import sys
import numpy as np
from functions import Obj, Camera, render_scene, load_json_obj, draw_impostor_sphere
from controls import get_movement_input, get_rotation_input
from char import Char_to_Object

# Parse arguments
parser = argparse.ArgumentParser(description="Basic 3D Engine")
parser.add_argument("-s", "--string", type=str, help="String to render as 3D text")
args = parser.parse_args()

pygame.init()

# Setup fullscreen display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Basic-3D Engine")

clock = pygame.time.Clock()
fps = 60

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

# Scene Configuration
SCENE_NAMES = [
    "UV Sphere",
    "3D Text Engine",
    "Penguin Model",
    "Single Impostor Sphere",
    "Impostor Sphere Grid"
]

active_scene = 1 if args.string else 0
text_string = args.string if args.string else "3D ENGINE"

def get_scene_object(scene_idx):
    obj = Obj()
    if scene_idx == 0:
        obj.Generate_Unit_Sphere(scale_factor=200)
    elif scene_idx == 1:
        spacing = 150
        start_x = -((len(text_string) * spacing) / 2)
        for i, char in enumerate(text_string):
            char_converter = Char_to_Object(char)
            char_obj = char_converter.make_object(scale_factor=12)
            char_obj.Translate(np.array([start_x + (i * spacing), 0.0, 0.0]))
            
            vertex_offset = len(obj.Points)
            obj.Points.extend(char_obj.Points)
            for face in char_obj.Faces:
                obj.Faces.append((face[0]+vertex_offset, face[1]+vertex_offset, face[2]+vertex_offset))
        obj.Populate_Edges_From_Faces()
    elif scene_idx == 2:
        try:
            # Penguin model
            obj = load_json_obj("penger.json", scale=2.0)
        except Exception:
            # Fallback if not found
            obj.Generate_Unit_Sphere(scale_factor=200)
    elif scene_idx == 3:
        obj.Generate_Single_Node(radius=150.0)
    elif scene_idx == 4:
        obj.Generate_Impostor_Grid(scale_factor=300, grid_size=3)
    return obj

main_obj = get_scene_object(active_scene)

# Camera Setup
camera = Camera(np.array([0.0, 0.0, -1000.0 if active_scene in [1, 2] else -600.0]))
focal_length = 600

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
            elif event.key == pygame.K_o:
                active_scene = (active_scene + 1) % len(SCENE_NAMES)
                main_obj = get_scene_object(active_scene)
                # Reset camera position depending on scene for best viewing distance
                if active_scene in [1, 2]: # Text, Penguin
                    camera.Coordinates = np.array([0.0, 0.0, -1000.0])
                else: # Sphere, single impostor, grid
                    camera.Coordinates = np.array([0.0, 0.0, -600.0])

    # Keyboard continuous input for camera controls
    dx, dy, dz = get_movement_input()
    rx, ry = get_rotation_input()
    
    move_speed = 20.0 if active_scene in [1, 2] else 10.0
    camera.Translate(np.array([dx * move_speed, dy * move_speed, dz * move_speed]))
    
    if rx != 0:
        camera.Rotate(rx * 2.0, 1)
    if ry != 0:
        camera.Rotate(ry * 2.0, 0)

    # Fill background based on active theme
    screen.fill(active_theme["background"])

    # Auto-rotation for dynamic effect
    if active_scene != 1:  # Rotate everything except the text layout
        main_obj.Rotate(1.2, 1)
        main_obj.Rotate(0.4, 0)

    # Render scene using our unified rendering pipeline
    render_scene(screen, width, height, camera, focal_length, main_obj, render_config, active_theme)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()
