import sys
import json
import pygame
import numpy as np
from functions import Obj, Camera, Point, render_scene, load_json_obj
from controls import get_movement_input, get_rotation_input

def main():
    if len(sys.argv) < 2:
        print("Usage: python display.py <json_filepath>")
        sys.exit(1)
        
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
        
        move_speed = 20.0
        local_move = np.array([dx * move_speed, dy * move_speed, dz * move_speed])
        world_move = np.dot(camera.Orientation, local_move)
        camera.Translate(world_move)
        
        if rx != 0:
            camera.Rotate(rx * 2.0, 1)
        if ry != 0:
            camera.Rotate(ry * 2.0, 0)

        # Fill background based on active theme
        screen.fill(active_theme["background"])

        # Auto-rotation
        target_obj.Rotate(1.5, 1)

        # Render using the unified engine
        render_scene(screen, width, height, camera, focal_length, target_obj, render_config, active_theme)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
