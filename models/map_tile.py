from lib.constants import *
from models.sprite import Sprite
from models.text import Text

class MapTile(object):
        # MapTile(self.scene, map_data['terrains'][self.map_data[h][w]['terrain_index']], self.tile_height_and_width, h, w)
  def __init__(self, scene, terrain, h_and_w, map_tile_x, map_tile_y):
    self.scene = scene
    self.x = None
    self.y = None
    self.h = round(h_and_w * HEIGHT_SCALER)
    self.w = round(h_and_w * HEIGHT_SCALER)
    self.map_tile_x = map_tile_x
    self.map_tile_y = map_tile_y
    self.map_x, self.map_y = self.scene.get_map_x_and_map_y_from_tile(self)
    self.sprite = Sprite(scene, terrain, self.x, self.y, ZOrder.Background, self.h, self.w, 1)
    self.map_text  = Text(scene, str(self.map_tile_x) + ',' + str(self.map_tile_y), self.x, self.y, Z_ORDER.BackgroundUI)
    self.map_text2 = Text(scene, str(self.map_x) + ',' + str(self.map_y), self.x, self.y, Z_ORDER.BackgroundUI)
    self.h_h = round(self.h // 2)
    self.h_w = round(self.w // 2)

  def on_update(self):
    self.x, self.y = self.scene.get_x_and_y_pos_from_camera(self)
    self.sprite.on_update(self.x, self.y)
    self.map_text.on_update(self.x, self.y)
    self.map_text2.on_update(self.x, self.y + 30)

  def on_draw(self):
    return self.sprite

  def on_draw_text(self):
    return [self.map_text, self.map_text2]