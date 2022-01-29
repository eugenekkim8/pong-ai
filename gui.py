from pong import Pong
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    KEYDOWN,
    KEYUP
)

pygame.init()
clock = pygame.time.Clock()

g = Pong()

screen = pygame.display.set_mode((g.WIDTH, g.HEIGHT))
screen.fill((255, 255, 255))

P1 = pygame.Surface((g.P1.w, g.P1.h))
P1r = P1.get_rect()
P1.fill((0, 0, 0))

P2 = pygame.Surface((g.P2.w, g.P2.h))
P2r = P2.get_rect()
P2.fill((0, 0, 0))

B = pygame.Surface((g.B.w, g.B.h))
Br = B.get_rect()
B.fill((0, 0, 0))

is_active = True

while (is_active):

    screen.fill((255, 255, 255))

    pressed_keys = pygame.key.get_pressed()
    action = ""
    if pressed_keys[K_UP]:
        action = 'u'
    elif pressed_keys[K_DOWN]:
        action = 'd'

    screen.blit(P1, (g.P1.x, g.P1.y))
    screen.blit(P2, (g.P2.x, g.P2.y))
    screen.blit(B, (g.B.x, g.B.y))

    game_info = g.step(action)
    is_active = not game_info[2]

    clock.tick(50)

    pygame.display.update()
    pygame.event.pump()

print(game_info)