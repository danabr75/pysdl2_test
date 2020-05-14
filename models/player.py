from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
    K_w,
    K_a,
    K_s,
    K_d
)

import pygame
# from ..lib.z_order import Player

class Player(pygame.sprite.Sprite):
  SPEED = 0.1

  def __init__(self, x, y):
    super(Player, self).__init__()
    self.surf = pygame.Surface((75, 25))
    self.surf.fill((255, 125, 255))
    self.rect = self.surf.get_rect()
    self.move_left = False
    self.move_right = False
    self.move_up = False
    self.move_down = False
    self.x = x
    self.y = y

  def event_update(self, event):
    if event.type == KEYDOWN:
      if event.key == K_w:
        self.move_up = True
      if event.key == K_s:
        self.move_down = True
      if event.key == K_d:
        self.move_right = True
      if event.key == K_a:
        self.move_left = True
    elif event.type == KEYUP:
      if event.key == K_w:
        self.move_up = False
      if event.key == K_s:
        self.move_down = False
      if event.key == K_d:
        self.move_right = False
      if event.key == K_a:
        self.move_left = False


  def update(self):
    if self.move_left:
      self.x -= self.SPEED
    if self.move_right:
      self.x += self.SPEED
    if self.move_up:
      self.y -= self.SPEED
    if self.move_down:
      self.y += self.SPEED

  def draw(self, screen):
    screen.blit(self.surf, (self.x, self.y))
