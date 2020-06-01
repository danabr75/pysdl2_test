from lib.constants import *
from models.sprite import Sprite
from models.text import Text

class MapTile(object):
  def __init__(self, scene, terrain, x, y, h_and_w, map_x, map_y):
    self.x = x
    self.y = y
    self.h = round(h_and_w * HEIGHT_SCALER)
    self.w = round(h_and_w * HEIGHT_SCALER)
    self.map_x = map_x
    self.map_y = map_y
    self.sprite = Sprite(scene, terrain, self.x, self.y, ZOrder.Background, self.h, self.w, 1)
    self.map_text = Text(scene, str(map_x) + ',' + str(map_y), self.x, self.y, Z_ORDER.BackgroundUI)

  def on_update(self, x, y):
    # print("MAP TILE UPDATE: " + str([x, y]))
    self.x = x
    self.y = y
    # Update in position to the Camera.
    self.sprite.on_update(self.x, self.y)
    self.map_text.on_update(self.x, self.y)

  def on_draw(self):
    return self.sprite

  def on_draw_text(self):
    return self.map_text.on_draw_text()