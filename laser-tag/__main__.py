import pygame
from pygame.locals import *

print("Hello world!")
print(__name__)


screen = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Laser Tag")

screen.fill((42, 42, 42))


running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    pygame.display.flip()

pygame.quit()
