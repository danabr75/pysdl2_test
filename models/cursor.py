from pygame.locals import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
)

import pygame
# from ..lib.z_order import Player

class Cursor(pygame.sprite.Sprite):
  def __init__(self):
    super(Cursor, self).__init__()
    self.unclicked_surf = pygame.Surface((25, 25))
    self.unclicked_surf.fill((0, 125, 255))
    self.clicked_surf = pygame.Surface((25, 25))
    self.clicked_surf.fill((100, 125, 0))
    self.active_surf = self.unclicked_surf
    self.is_clicked = False
    self.click_held = False

  def event_update(self, event):
    if event.type == MOUSEBUTTONDOWN:
      print("CLICKED")
      self.is_clicked = True
      self.click_held = True
      # call clicked on object at cooards?
    elif event.type == MOUSEBUTTONUP:
      print("UNCLICKED")
      self.click_held = False

  def update(self):
    self.is_clicked = False
    if self.click_held:
      self.active_surf = self.clicked_surf
    else:
      self.active_surf = self.unclicked_surf


  def draw(self, screen):
    screen.blit(self.active_surf, pygame.mouse.get_pos())
