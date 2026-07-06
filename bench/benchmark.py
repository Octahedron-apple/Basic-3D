import os
import sys
import time
import numpy as np

# Ensure root directory is in search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
pygame.init()

from functions import Obj, Camera, Point, load_json_obj
from char import Char_to_Object

# Custom instrumented render function to measure math/projection vs. pygame draw calls
def instrumented_render_scene(screen, width, height, camera, focal_length, objects_with_colors, render_config, theme):
    if not isinstance(objects_with_colors, list):
        objects_with_colors = [(objects_with_colors, None)]
    elif len(objects_with_colors) > 0 and not isinstance(objects_with_colors[0], tuple):
        objects_with_colors = [(o, None) for o in objects_with_colors]
        
    t_start = time.perf_counter()
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
            
        if render_config.get("faces", True) and len(obj.Faces) > 0:
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
        
        if render_config.get("lines", True) and (not render_config.get("faces", True) or len(obj.Faces) == 0):
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
    t_calc_end = time.perf_counter()
    
    # Draw phase
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
                pygame.draw.circle(screen, n_col, center, r_2d)

    t_draw_end = time.perf_counter()
    
    calc_time = t_calc_end - t_start
    draw_time = t_draw_end - t_calc_end
    return calc_time, draw_time

def run_benchmark():
    screen = pygame.display.set_mode((1920, 1080))
    width, height = 1920, 1080
    focal_length = 600
    camera = Camera(np.array([0.0, -200.0, -1000.0]))
    theme = {"face": (40, 20, 80), "line": (0, 255, 240), "node": (255, 0, 128)}
    
    # Pre-generate scenes
    # Scene 1: UV Sphere
    sphere_obj = Obj().Generate_Unit_Sphere(scale_factor=200, lat_count=12, lon_count=24)
    
    # Scene 2: 3D Text
    text_string = "BENCHMARK"
    text_obj = Obj()
    spacing = 150
    start_x = -((len(text_string) * spacing) / 2)
    for i, char in enumerate(text_string):
        char_converter = Char_to_Object(char)
        char_obj = char_converter.make_object(scale_factor=12)
        char_obj.Translate(np.array([start_x + (i * spacing), 0.0, 0.0]))
        vertex_offset = len(text_obj.Points)
        text_obj.Points.extend(char_obj.Points)
        for face in char_obj.Faces:
            text_obj.Faces.append((face[0]+vertex_offset, face[1]+vertex_offset, face[2]+vertex_offset))
    text_obj.Populate_Edges_From_Faces()
    
    # Scene 3: Solar System Frame Mockup (Sun + 5 planets + orbits + 800 debris asteroids)
    solar_objs = []
    # Sun
    sun = Obj()
    sun.Points.append(Point(np.array([0., 0., 0.]), Radius=75.0))
    solar_objs.append((sun, (None, None, (255, 200, 0))))
    
    # 5 dwarf planets
    for dp_dist in [2.77, 39.48, 43.13, 45.43, 67.78]:
        dp = Obj()
        dp.Points.append(Point(np.array([dp_dist * 100, 0., 0.]), Radius=10.0))
        solar_objs.append((dp, (None, None, (200, 200, 200))))
        
    # Orbit tracks
    for dp_dist in [2.77, 39.48, 43.13, 45.43, 67.78]:
        vis_d = 75.0 + np.log10(1.0 + dp_dist) * 450.0
        orbit = Obj()
        for deg in range(0, 360, 5):
            rad = np.radians(deg)
            orbit.Points.append(Point(np.array([vis_d * np.cos(rad), 0., vis_d * np.sin(rad)]), Radius=1.5))
        for j in range(len(orbit.Points)):
            orbit.Edges.append((j, (j+1)%len(orbit.Points)))
        solar_objs.append((orbit, (False, (50, 50, 70), (45, 50, 65))))
        
    # 800 Debris asteroids
    asteroids = Obj()
    for _ in range(800):
        pos = np.random.normal(0, 300, size=3)
        asteroids.Points.append(Point(pos, Radius=1.0))
    solar_objs.append((asteroids, (False, False, (150, 150, 150))))
    
    # Scene 4: Penger Setup (Penguin + Text "PENGER")
    penger_obj = load_json_obj("penger.json")
    penger_obj.Scale(2.0)
    penger_text_obj = Obj()
    penger_string = "PENGER"
    p_start_x = -((len(penger_string) * spacing) / 2)
    for i, char in enumerate(penger_string):
        char_converter = Char_to_Object(char)
        char_obj = char_converter.make_object(scale_factor=12)
        char_obj.Translate(np.array([p_start_x + (i * spacing), 0.0, 0.0]))
        vertex_offset = len(penger_text_obj.Points)
        penger_text_obj.Points.extend(char_obj.Points)
        for face in char_obj.Faces:
            penger_text_obj.Faces.append((face[0]+vertex_offset, face[1]+vertex_offset, face[2]+vertex_offset))
    penger_text_obj.Populate_Edges_From_Faces()
    penger_text_obj.Translate(np.array([75.0, 300.0, 0.0]))
    penger_objs = [
        (penger_obj, (None, None, None)),
        (penger_text_obj, (None, None, None))
    ]
    
    # Scene 5: test_chars.py Mockup (Text "Demo Testing")
    demo_testing_string = "Demo Testing"
    demo_testing_objs = []
    dt_spacing = 150
    dt_start_x = -((len(demo_testing_string) * dt_spacing) / 2)
    for i, char in enumerate(demo_testing_string):
        char_converter = Char_to_Object(char)
        char_obj = char_converter.make_object(scale_factor=12)
        char_obj.Translate(np.array([dt_start_x + (i * dt_spacing), 0.0, 0.0]))
        char_obj.Populate_Edges_From_Faces()
        demo_testing_objs.append((char_obj, (None, None, None)))
        
    # fontgen font atlas generation workload function
    def fontgen_workload():
        pygame.font.init()
        font = pygame.font.SysFont('Courier', 20, bold=True) 
        characters_to_generate = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!? "
        font_data = {}
        for char in characters_to_generate:
            surf = font.render(char, True, (255, 255, 255), (0, 0, 0))
            width, height = surf.get_size()
            
            grid = []
            for y in range(height):
                row = []
                for x in range(width):
                    row.append(surf.get_at((x, y))[0] > 128)
                grid.append(row)
                
            char_points = []
            char_faces = []
            vertex_count = 0
            
            for y in range(height):
                for x in range(width):
                    if grid[y][x]:
                        w = 1
                        while x + w < width and grid[y][x + w]:
                            w += 1
                        
                        h = 1
                        can_expand = True
                        while y + h < height and can_expand:
                            for ix in range(w):
                                if not grid[y + h][x + ix]:
                                    can_expand = False
                                    break
                            if can_expand:
                                h += 1
                        
                        for iy in range(h):
                            for ix in range(w):
                                grid[y + iy][x + ix] = False
                                
                        pos_x = x - (width / 2.0)
                        pos_y = y - (height / 2.0) 
                        
                        pts = [
                            [pos_x, pos_y, -0.5], [pos_x+w, pos_y, -0.5], [pos_x+w, pos_y+h, -0.5], [pos_x, pos_y+h, -0.5],
                            [pos_x, pos_y,  0.5], [pos_x+w, pos_y,  0.5], [pos_x+w, pos_y+h,  0.5], [pos_x, pos_y+h,  0.5]
                        ]
                        fcs = [
                            [0,1,2], [0,2,3], [5,4,7], [5,7,6],
                            [4,0,3], [4,3,7], [1,5,6], [1,6,2],
                            [3,2,6], [3,6,7], [4,5,1], [4,1,0]
                        ]
                        
                        char_points.extend(pts)
                        for f in fcs:
                            char_faces.append([f[0]+vertex_count, f[1]+vertex_count, f[2]+vertex_count])
                        vertex_count += 8
            font_data[char] = {"points": char_points, "faces": char_faces}
    
    # Configurations to profile
    configs = {
        "UV Sphere (Faces + Edges + Nodes)": (sphere_obj, {"faces": True, "lines": True, "nodes": True}, 200),
        "3D Text Engine (Faces + Edges)": (text_obj, {"faces": True, "lines": True, "nodes": False}, 200),
        "Solar System Mock (Orbits + 800 Nodes)": (solar_objs, {"faces": True, "lines": True, "nodes": True}, 200),
        "Penguin Showcase (penger.py Mock)": (penger_objs, {"faces": True, "lines": True, "nodes": True}, 200),
        "Character Test (test_chars.py - Demo Testing)": (demo_testing_objs, {"faces": True, "lines": True, "nodes": True}, 200)
    }
    
    results = {}
    
    # Run 3D Rendering benchmarks
    for name, (objs, cfg, frames) in configs.items():
        print(f"Benchmarking {name} for {frames} frames...")
        calc_times = []
        draw_times = []
        
        for frame in range(frames):
            # Process event queue to prevent OS window freeze
            for event in pygame.event.get():
                pass
            
            # Clear screen
            screen.fill((10, 10, 20))
            
            # Apply continuous rotation to represent active dynamic updates
            if isinstance(objs, list):
                for o_tuple in objs:
                    o = o_tuple[0]
                    o.Rotate(1.0, 1)
            else:
                objs.Rotate(1.0, 1)
                
            calc_t, draw_t = instrumented_render_scene(screen, width, height, camera, focal_length, objs, cfg, theme)
            
            # Draw to display
            pygame.display.flip()
            
            calc_times.append(calc_t)
            draw_times.append(draw_t)
            
        avg_calc = np.mean(calc_times) * 1000  # ms
        avg_draw = np.mean(draw_times) * 1000  # ms
        total_frame = avg_calc + avg_draw
        
        # Calculate 10% and 1% low FPS values
        frame_times = [c + d for c, d in zip(calc_times, draw_times)]
        fps_list = [1.0 / ft if ft > 0 else float('inf') for ft in frame_times]
        sorted_fps = sorted(fps_list)
        low_10_fps = sorted_fps[int(len(sorted_fps) * 0.10)]
        low_1_fps = sorted_fps[int(len(sorted_fps) * 0.01)]
        
        results[name] = {
            "avg_calc_ms": avg_calc,
            "avg_draw_ms": avg_draw,
            "total_frame_ms": total_frame,
            "fps_cap": 1000.0 / total_frame if total_frame > 0 else float('inf'),
            "low_10_fps": low_10_fps,
            "low_1_fps": low_1_fps
        }
        
    # Benchmark CPU fontgen workload
    print("Benchmarking Font Generation Atlas (fontgen) for 5 runs...")
    fontgen_times = []
    for _ in range(5):
        t_start = time.perf_counter()
        fontgen_workload()
        fontgen_times.append(time.perf_counter() - t_start)
    avg_fontgen = np.mean(fontgen_times) * 1000
    
    results["Font Generation Atlas (fontgen)"] = {
        "avg_calc_ms": avg_fontgen,
        "avg_draw_ms": 0.0,
        "total_frame_ms": avg_fontgen,
        "fps_cap": 1000.0 / avg_fontgen if avg_fontgen > 0 else float('inf'),
        "low_10_fps": 1000.0 / avg_fontgen if avg_fontgen > 0 else float('inf'),
        "low_1_fps": 1000.0 / avg_fontgen if avg_fontgen > 0 else float('inf')
    }
        
    out_dir = os.path.dirname(os.path.abspath(__file__))
    results_file = os.path.join(out_dir, "results.md")
    
    with open(results_file, "w") as f:
        f.write("# Benchmark Results\n\n")
        f.write("Performance profiling comparing 3D projection, depth sorting, and topological calculation time vs. actual Pygame graphics drawing time. Run on a headless configuration.\n\n")
        f.write("| Scene / Workload | Math & Sort Calc (ms) | Pygame Draw Call (ms) | Total Frame (ms) | Avg FPS | 10% Low FPS | 1% Low FPS |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- |\n")
        for name, data in results.items():
            f.write(f"| {name} | {data['avg_calc_ms']:.3f} | {data['avg_draw_ms']:.3f} | {data['total_frame_ms']:.3f} | {data['fps_cap']:.1f} | {data['low_10_fps']:.1f} | {data['low_1_fps']:.1f} |\n")
            
    print(f"\nBenchmark completed successfully!")
    print(f"Results written to: {results_file}\n")
    print(f"{'Scene':<46} | {'Math & Sort':<12} | {'Pygame Draw':<12} | {'Total':<10} | {'Avg FPS':<8} | {'10% Low':<8} | {'1% Low':<6}")
    print("-" * 119)
    for name, data in results.items():
        print(f"{name:<46} | {data['avg_calc_ms']:>10.3f}ms | {data['avg_draw_ms']:>10.3f}ms | {data['total_frame_ms']:>8.3f}ms | {data['fps_cap']:>7.1f} | {data['low_10_fps']:>7.1f} | {data['low_1_fps']:>5.1f}")
    print()

if __name__ == "__main__":
    run_benchmark()
