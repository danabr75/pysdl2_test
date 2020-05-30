from lib.constants import *
from models.sprite import Sprite

class MapTile(object):

  def __init__(self, scene, terrain, x, y):
    self.x = x
    self.y = y
    self.sprite = Sprite(scene, terrain, self.x, self.y)

  def on_update(self, x, y):
    # print("MAP TILE UPDATE: " + str([x, y]))
    self.x = x
    self.y = y
    # Update in position to the Camera.
    self.sprite.on_update(self.x, self.y)

  def on_draw(self):
    return self.sprite.on_draw()