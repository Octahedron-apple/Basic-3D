import pygame
import json

pygame.font.init()

def create_box_data(x, y, w, h):
    points = [
        [x, y, -0.5], [x+w, y, -0.5], [x+w, y+h, -0.5], [x, y+h, -0.5],
        [x, y,  0.5], [x+w, y,  0.5], [x+w, y+h,  0.5], [x, y+h,  0.5]
    ]
    faces = [
        [0,1,2], [0,2,3], [5,4,7], [5,7,6],
        [4,0,3], [4,3,7], [1,5,6], [1,6,2],
        [3,2,6], [3,6,7], [4,5,1], [4,1,0]
    ]
    return points, faces

font_data = {}
font = pygame.font.SysFont('Courier', 20, bold=True) 
characters_to_generate = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!? "
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
                
                pts, fcs = create_box_data(pos_x, pos_y, w, h)
                
                char_points.extend(pts)
                for f in fcs:
                    char_faces.append([f[0]+vertex_count, f[1]+vertex_count, f[2]+vertex_count])
                vertex_count += 8

    font_data[char] = {"points": char_points, "faces": char_faces}

with open("default_font.json", "w") as f:
    json.dump(font_data, f, indent=4)

print("Saved successfully to default_font.json!")
