# Frogger
import pygame


pygame.init()

WIDTH = 1000
HEIGHT = 750
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
# ------------------------------------
# Functions

# ------------------------------------
# Global Variables

# ------------------------------------
# Game Loop
running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)
    # ------------------------------------
    

pygame.quit()
