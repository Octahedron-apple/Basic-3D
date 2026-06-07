import pygame
import sys
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("")
clock = pygame.time.Clock()
fps = 60
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
sys.exit()
