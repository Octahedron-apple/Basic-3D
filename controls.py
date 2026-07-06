import pygame

def get_movement_input():
    keys = pygame.key.get_pressed()
    
    left = keys[pygame.K_a]
    right = keys[pygame.K_d]
    
    forward = keys[pygame.K_w]
    backward = keys[pygame.K_s]
    
    up = keys[pygame.K_SPACE]
    down = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    
    dx = 0
    dy = 0
    dz = 0
    
    if left: dx -= 1
    if right: dx += 1
    if up: dy -= 1 
    if down: dy += 1
    if forward: dz += 1
    if backward: dz -= 1
        
    return dx, dy, dz

def get_rotation_input():
    keys = pygame.key.get_pressed()
    
    left = keys[pygame.K_LEFT]
    right = keys[pygame.K_RIGHT]
    up = keys[pygame.K_UP]
    down = keys[pygame.K_DOWN]
    
    rx = 0
    ry = 0
    
    if left: rx -= 1
    if right: rx += 1
    if up: ry -= 1 
    if down: ry += 1
        
    return rx, ry
