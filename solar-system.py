import pygame
import sys
import numpy as np
from functions import Obj, Camera, Point, render_scene

# Dwarf Planets Data
# Distance in AU, Orbit in Earth Years, Inclination in degrees, Visual Radius in pixels, and colors.
DWARF_PLANETS = [
    {
        "name": "Ceres",
        "distance": 2.77,
        "orbit": 4.60,
        "inclination": 10.59,
        "color": (160, 160, 165),
        "visual_radius": 6.0
    },
    {
        "name": "Pluto",
        "distance": 39.482,
        "orbit": 247.94,
        "inclination": 17.16,
        "color": (180, 160, 150),
        "visual_radius": 9.0
    },
    {
        "name": "Haumea",
        "distance": 43.13,
        "orbit": 283.0,
        "inclination": 28.19,
        "color": (210, 210, 215),
        "visual_radius": 8.0
    },
    {
        "name": "Makemake",
        "distance": 45.43,
        "orbit": 306.0,
        "inclination": 29.00,
        "color": (190, 110, 80),
        "visual_radius": 8.0
    },
    {
        "name": "Eris",
        "distance": 67.78,
        "orbit": 558.0,
        "inclination": 44.00,
        "color": (225, 225, 230),
        "visual_radius": 9.0
    }
]

pygame.init()

# Setup fullscreen display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Solar System 3D Minor Bodies Simulator")

clock = pygame.time.Clock()
fps = 60

# Setup label font
try:
    label_font = pygame.font.SysFont("sans-serif", 13)
except Exception:
    label_font = pygame.font.Font(None, 16)

# Visualization scales
sun_visual_radius = 75.0

def get_visual_distance(dist_au):
    if dist_au <= 0:
        return 0.0
    return sun_visual_radius + np.log10(1.0 + dist_au) * 450.0

def generate_orbit_object(distance, inclination_deg, num_segments=128):
    """
    Generates a circular orbit path tilted by inclination.
    It contains both Points and Edges, rendering as 'points and lines'.
    """
    obj = Obj()
    inc_rad = np.radians(inclination_deg)
    vis_d = get_visual_distance(distance)
    
    for i in range(num_segments):
        theta = i * 2 * np.pi / num_segments
        # Orbit in X-Z plane
        x = vis_d * np.cos(theta)
        z = vis_d * np.sin(theta)
        # Tilt orbit around X-axis
        y_inclined = z * np.sin(inc_rad)
        z_inclined = z * np.cos(inc_rad)
        
        # Add tiny nodes along the orbit path so they render as points
        obj.Points.append(Point(np.array([x, y_inclined, z_inclined]), Radius=1.5))
        
    for i in range(num_segments):
        obj.Edges.append((i, (i + 1) % num_segments))
        
    return obj

# Pre-generate orbits for Dwarf Planets
orbit_objects = []
for dp in DWARF_PLANETS:
    orbit_objects.append(generate_orbit_object(dp["distance"], dp["inclination"]))

# --- Particle Populations Initialization ---
np.random.seed(42)

# 1. Main Asteroid Belt (2.2 to 3.2 AU)
NUM_ASTEROIDS = 300
asteroids_data = []
for _ in range(NUM_ASTEROIDS):
    d = np.random.uniform(2.2, 3.2)
    inc = np.random.normal(0, 3.0)
    node = np.random.uniform(0, 2 * np.pi)
    phase = np.random.uniform(0, 2 * np.pi)
    period = d ** 1.5
    asteroids_data.append((d, inc, node, phase, period))

# 2. Jupiter Trojans (Co-orbital, sharing path at 5.20 AU, 60 degrees ahead and behind)
NUM_TROJANS = 100
trojans_L4_data = []
trojans_L5_data = []
for _ in range(NUM_TROJANS):
    # L4 (+60 deg)
    d_l4 = np.random.normal(5.20, 0.15)
    dtheta_l4 = np.random.normal(0, np.radians(8.0))
    inc_l4 = np.random.normal(0, 5.0)
    node_l4 = np.random.uniform(0, 2 * np.pi)
    trojans_L4_data.append((d_l4, dtheta_l4, inc_l4, node_l4))
    
    # L5 (-60 deg)
    d_l5 = np.random.normal(5.20, 0.15)
    dtheta_l5 = np.random.normal(0, np.radians(8.0))
    inc_l5 = np.random.normal(0, 5.0)
    node_l5 = np.random.uniform(0, 2 * np.pi)
    trojans_L5_data.append((d_l5, dtheta_l5, inc_l5, node_l5))

# 3. Centaurs (5.2 to 30.0 AU)
NUM_CENTAURS = 120
centaurs_data = []
for _ in range(NUM_CENTAURS):
    d = np.random.uniform(5.2, 30.0)
    inc = np.random.normal(0, 15.0)
    node = np.random.uniform(0, 2 * np.pi)
    phase = np.random.uniform(0, 2 * np.pi)
    period = d ** 1.5
    centaurs_data.append((d, inc, node, phase, period))

# 4. Kuiper Belt (30.0 to 50.0 AU)
NUM_KUIPER = 350
kuiper_data = []
for _ in range(NUM_KUIPER):
    d = np.random.uniform(30.0, 50.0)
    inc = np.random.normal(0, 8.0)
    node = np.random.uniform(0, 2 * np.pi)
    phase = np.random.uniform(0, 2 * np.pi)
    period = d ** 1.5
    kuiper_data.append((d, inc, node, phase, period))

# 5. Short-Period Comets (Aphelion at 30 to 50 AU, highly eccentric)
NUM_SHORT_COMETS = 20
short_comets_data = []
for _ in range(NUM_SHORT_COMETS):
    q = np.random.uniform(0.5, 2.5)       # Perihelion
    Q = np.random.uniform(30.0, 50.0)     # Aphelion
    a = (q + Q) / 2.0
    e = (Q - q) / (Q + q)
    inc = np.random.uniform(5.0, 35.0)
    node = np.random.uniform(0, 2 * np.pi)
    phase = np.random.uniform(0, 2 * np.pi)
    period = a ** 1.5
    short_comets_data.append((a, e, inc, node, phase, period))

# 6. Long-Period Comets (Aphelion at 2000+ AU)
NUM_LONG_COMETS = 15
long_comets_data = []
for _ in range(NUM_LONG_COMETS):
    q = np.random.uniform(0.5, 4.0)        # Perihelion
    Q = np.random.uniform(2000.0, 8000.0)  # Aphelion
    a = (q + Q) / 2.0
    e = (Q - q) / (Q + q)
    inc = np.random.uniform(20.0, 80.0)
    node = np.random.uniform(0, 2 * np.pi)
    phase = np.random.uniform(0, 2 * np.pi)
    period = a ** 1.5
    long_comets_data.append((a, e, inc, node, phase, period))

# 7. Oort Cloud (Spherical shell at 2000 to 8000 AU, static)
NUM_OORT = 400
oort_points = []
for _ in range(NUM_OORT):
    d = np.random.uniform(2000.0, 8000.0)
    vis_d = get_visual_distance(d)
    
    # Choose random spherical coordinate
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    
    x = vis_d * np.sin(theta) * np.cos(phi)
    y = vis_d * np.sin(theta) * np.sin(phi)
    z = vis_d * np.cos(theta)
    
    oort_points.append(Point(np.array([x, y, z]), Radius=1.0))
oort_cloud_obj = Obj()
oort_cloud_obj.Points = oort_points

# Camera configuration: start tilted looking down at the ecliptic plane
camera = Camera(np.array([0.0, -900.0, -2200.0]))
camera.Rotate(22.0, 0)
focal_length = 600

# Render configuration
render_config = {
    "faces": True,
    "lines": True,
    "nodes": True,
    "node_style": "impostor",
    "default_node_radius": 6.0
}

active_theme = {
    "name": "Space",
    "background": (3, 3, 8),
    "face": (0, 0, 0),
    "line": (40, 40, 60),
    "node": (255, 255, 255)
}

# Simulation settings
t = 0.0
time_scale = 2.0  # Speed up by default for slow outer bodies
paused = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_LEFTBRACKET:
                time_scale = max(0.01, time_scale / 1.5)
            elif event.key == pygame.K_RIGHTBRACKET:
                time_scale = min(100.0, time_scale * 1.5)
            elif event.key == pygame.K_MINUS:
                focal_length = max(100, focal_length - 25)
            elif event.key == pygame.K_EQUALS:
                focal_length = min(3000, focal_length + 25)

    # Keyboard continuous movements
    keys = pygame.key.get_pressed()
    dx, dy, dz, rx, ry = 0, 0, 0, 0, 0
    
    if keys[pygame.K_a]: dx -= 1
    if keys[pygame.K_d]: dx += 1
    if keys[pygame.K_w]: dz += 1
    if keys[pygame.K_s]: dz -= 1
    if keys[pygame.K_SPACE]: dy -= 1
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]: dy += 1
    if keys[pygame.K_LEFT]: rx -= 1
    if keys[pygame.K_RIGHT]: rx += 1
    if keys[pygame.K_UP]: ry -= 1
    if keys[pygame.K_DOWN]: ry += 1

    move_speed = 25.0
    local_move = np.array([dx * move_speed, dy * move_speed, dz * move_speed])
    world_move = np.dot(camera.Orientation, local_move)
    camera.Translate(world_move)
    
    if rx != 0:
        camera.Rotate(rx * 2.0, 1)
    if ry != 0:
        camera.Rotate(ry * 2.0, 0)

    # Tick simulation clock
    dt = clock.tick(fps) / 1000.0
    if not paused:
        t += dt * time_scale

    # Clear screen
    screen.fill(active_theme["background"])

    # Build dynamically updating scene list
    scene_objects = []

    # 1. Add Orbit Paths (both edges and nodes will be drawn)
    orbit_line_color = (40, 45, 60)
    orbit_node_color = (45, 50, 65)
    for orbit_obj in orbit_objects:
        scene_objects.append((orbit_obj, (False, orbit_line_color, orbit_node_color)))

    # 2. Add Oort Cloud (static background cloud)
    scene_objects.append((oort_cloud_obj, (False, False, (90, 110, 130))))

    # 3. Add Sun
    sun_pos = np.array([0.0, 0.0, 0.0])
    sun_obj = Obj()
    sun_obj.Points.append(Point(sun_pos, Radius=sun_visual_radius))
    scene_objects.append((sun_obj, (None, None, (255, 180, 0))))

    # 4. Add Asteroid Belt (2.2 to 3.2 AU)
    asteroid_belt_points = []
    for d, inc, node, phase, period in asteroids_data:
        theta = (2 * np.pi * t) / period + phase
        inc_rad = np.radians(inc)
        x_flat = d * np.cos(theta)
        z_flat = d * np.sin(theta)
        x = x_flat * np.cos(node) - z_flat * np.sin(node)
        z = x_flat * np.sin(node) + z_flat * np.cos(node)
        y = z * np.sin(inc_rad)
        z = z * np.cos(inc_rad)
        
        vis_d = get_visual_distance(d)
        pos = np.array([x, y, z]) / d * vis_d
        asteroid_belt_points.append(Point(pos, Radius=1.0))
    asteroid_belt_obj = Obj()
    asteroid_belt_obj.Points = asteroid_belt_points
    scene_objects.append((asteroid_belt_obj, (False, False, (120, 120, 120))))

    # 5. Add Trojans (L4 & L5 clusters sharing path at 5.2 AU)
    theta_j = (2 * np.pi * t) / 11.86
    trojan_points = []
    for is_l4, cluster_data in [(True, trojans_L4_data), (False, trojans_L5_data)]:
        center_angle = theta_j + np.pi/3 if is_l4 else theta_j - np.pi/3
        for d, dtheta, inc, node in cluster_data:
            theta = center_angle + dtheta
            inc_rad = np.radians(inc)
            x_flat = d * np.cos(theta)
            z_flat = d * np.sin(theta)
            x = x_flat * np.cos(node) - z_flat * np.sin(node)
            z = x_flat * np.sin(node) + z_flat * np.cos(node)
            y = z * np.sin(inc_rad)
            z = z * np.cos(inc_rad)
            
            vis_d = get_visual_distance(d)
            pos = np.array([x, y, z]) / d * vis_d
            trojan_points.append(Point(pos, Radius=1.0))
    trojans_obj = Obj()
    trojans_obj.Points = trojan_points
    scene_objects.append((trojans_obj, (False, False, (160, 130, 90))))

    # 6. Add Centaurs (5.2 to 30.0 AU)
    centaur_points = []
    for d, inc, node, phase, period in centaurs_data:
        theta = (2 * np.pi * t) / period + phase
        inc_rad = np.radians(inc)
        x_flat = d * np.cos(theta)
        z_flat = d * np.sin(theta)
        x = x_flat * np.cos(node) - z_flat * np.sin(node)
        z = x_flat * np.sin(node) + z_flat * np.cos(node)
        y = z * np.sin(inc_rad)
        z = z * np.cos(inc_rad)
        
        vis_d = get_visual_distance(d)
        pos = np.array([x, y, z]) / d * vis_d
        centaur_points.append(Point(pos, Radius=1.2))
    centaurs_obj = Obj()
    centaurs_obj.Points = centaur_points
    scene_objects.append((centaurs_obj, (False, False, (100, 130, 150))))

    # 7. Add Kuiper Belt (30.0 to 50.0 AU)
    kuiper_points = []
    for d, inc, node, phase, period in kuiper_data:
        theta = (2 * np.pi * t) / period + phase
        inc_rad = np.radians(inc)
        x_flat = d * np.cos(theta)
        z_flat = d * np.sin(theta)
        x = x_flat * np.cos(node) - z_flat * np.sin(node)
        z = x_flat * np.sin(node) + z_flat * np.cos(node)
        y = z * np.sin(inc_rad)
        z = z * np.cos(inc_rad)
        
        vis_d = get_visual_distance(d)
        pos = np.array([x, y, z]) / d * vis_d
        kuiper_points.append(Point(pos, Radius=1.2))
    kuiper_belt_obj = Obj()
    kuiper_belt_obj.Points = kuiper_points
    scene_objects.append((kuiper_belt_obj, (False, False, (150, 180, 220))))

    # 8. Add Comets (Short & Long Period)
    comet_points = []
    for is_long, comets_list in [(False, short_comets_data), (True, long_comets_data)]:
        for a, e, inc, node, phase, period in comets_list:
            M = (2 * np.pi * t) / period + phase
            E = M
            for _ in range(3):
                E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
                
            x_orb = a * (np.cos(E) - e)
            y_orb = a * np.sqrt(1.0 - e**2) * np.sin(E)
            
            x1 = x_orb * np.cos(node) - y_orb * np.sin(node)
            z1 = x_orb * np.sin(node) + y_orb * np.cos(node)
            y = z1 * np.sin(np.radians(inc))
            z = z1 * np.cos(np.radians(inc))
            
            r_au = np.sqrt(x1**2 + y**2 + z**2)
            vis_d = get_visual_distance(r_au)
            pos = np.array([x1, y, z]) / r_au * vis_d
            comet_points.append(Point(pos, Radius=1.5))
    comets_obj = Obj()
    comets_obj.Points = comet_points
    scene_objects.append((comets_obj, (False, False, (220, 240, 255))))

    # 9. Add Dwarf Planets
    planet_positions = {"Sun": sun_pos}
    for idx, dp in enumerate(DWARF_PLANETS):
        dist_pixels = get_visual_distance(dp["distance"])
        phase = idx * 0.7
        theta = (2 * np.pi * t) / dp["orbit"] + phase
        inc_rad = np.radians(dp["inclination"])
        
        x = dist_pixels * np.cos(theta)
        z_flat = dist_pixels * np.sin(theta)
        y = z_flat * np.sin(inc_rad)
        z = z_flat * np.cos(inc_rad)
        
        pos = np.array([x, y, z])
        planet_positions[dp["name"]] = pos
        
        p_obj = Obj()
        p_obj.Points.append(Point(pos, Radius=dp["visual_radius"]))
        scene_objects.append((p_obj, (None, None, dp["color"])))

    # Render scene
    render_scene(screen, width, height, camera, focal_length, scene_objects, render_config, active_theme)

    # Project and render text labels for Dwarf Planets and Sun (HUD is removed, only labels remain)
    inv_orientation = camera.Orientation.T
    for name, pos in planet_positions.items():
        rel_point = pos - camera.Coordinates
        aligned_point = np.dot(inv_orientation, rel_point)
        
        z_depth = aligned_point[2]
        if z_depth > 0.1:
            proj_x = focal_length * aligned_point[0] / z_depth
            proj_y = focal_length * aligned_point[1] / z_depth
            
            screen_x = int(width / 2 + proj_x)
            screen_y = int(height / 2 + proj_y)
            
            lbl_color = (255, 230, 150) if name == "Sun" else (200, 200, 210)
            txt_surf = label_font.render(name, True, lbl_color)
            screen.blit(txt_surf, (screen_x + 12, screen_y - 12))

    pygame.display.flip()

pygame.quit()
sys.exit()
