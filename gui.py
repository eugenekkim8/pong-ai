from pong import Pong
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    KEYDOWN,
    KEYUP
)

class PongGui:
    def __init__(self, game = None):
        self.g = game

        pygame.init()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.g.WIDTH, self.g.HEIGHT))
        self.screen.fill((255, 255, 255))

        self.P1 = pygame.Surface((self.g.P1.w, self.g.P1.h))
        self.P1r = self.P1.get_rect()
        self.P1.fill((0, 0, 0))

        self.P2 = pygame.Surface((self.g.P2.w, self.g.P2.h))
        self.P2r = self.P2.get_rect()
        self.P2.fill((0, 0, 0))

        self.B = pygame.Surface((self.g.B.w, self.g.B.h))
        self.Br = self.B.get_rect()
        self.B.fill((0, 0, 0))

    def render(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.P1, (self.g.P1.x, self.g.P1.y))
        self.screen.blit(self.P2, (self.g.P2.x, self.g.P2.y))
        self.screen.blit(self.B, (self.g.B.x, self.g.B.y))

        pygame.display.update()

g = Pong()
d = PongGui(g)

is_active = True

while (is_active):

    pressed_keys = pygame.key.get_pressed()
    action = ""
    if pressed_keys[K_UP]:
        action = 'u'
    elif pressed_keys[K_DOWN]:
        action = 'd'

    game_info = g.step(action)

    d.render()

    is_active = not game_info[2]

    d.clock.tick(50)
    pygame.event.pump()

# print(game_info)