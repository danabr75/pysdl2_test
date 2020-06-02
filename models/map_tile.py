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

     # int(object.map_tile_x * TILE_WIDTH_AND_HEIGHT), int(object.map_tile_y * TILE_WIDTH_AND_HEIGHT)
    self.map_x, self.map_y = self.scene.get_map_x_and_map_y_from_tile(self)
    self.sprite = Sprite(self.scene, terrain, self.x, self.y, ZOrder.Background, self.h, self.w, 1)
    self.map_text  = Text(self.scene, str(self.map_tile_x) + ',' + str(self.map_tile_y), self.x, self.y, Z_ORDER.BackgroundUI)
    self.map_text4 = Text(self.scene, str(self.map_x) + ',' + str(self.map_y), self.x, self.y, Z_ORDER.BackgroundUI)
    
    self.h_h = round(self.h // 2)
    self.h_w = round(self.w // 2)

    self.start_visible_map_x = None
    self.start_visible_map_y = None
    self.map_text2 = None
    self.debug_val = False

  def debug(self, start_visible_map_x, start_visible_map_y, debug_val = False):
    self.debug_val = debug_val
    self.start_visible_map_x = start_visible_map_x
    self.start_visible_map_y = start_visible_map_y
    self.map_text2 = Text(self.scene, "init: " + str(self.start_visible_map_x) + ',' + str(self.start_visible_map_y), 0, 0, Z_ORDER.BackgroundUI)

  def on_update(self, h, w):
    self.x, self.y = self.scene.get_x_and_y_pos_from_camera(self)
    if self.debug_val:
        # object.map_x
        print("GOT X,Y: " + str(self.x) + ',' + str(self.y) + " from map: " + str(self.map_x) + ',' + str(self.map_y))
        self.debug_val = False
    self.sprite.on_update(self.x, self.y)
    self.map_text.on_update(self.x, self.y)
    if self.map_text2:
        self.map_text2.on_update(self.x, self.y + 15)
    self.map_text3 = Text(self.scene, "now: " + str(h) + ',' + str(w), self.x, self.y + 30, Z_ORDER.BackgroundUI)
    self.map_text4.on_update(self.x, self.y + 45)

  def on_draw(self):
    return self.sprite

  def on_draw_text(self):
    if self.map_text2:
        return [self.map_text, self.map_text2, self.map_text3, self.map_text4]
    else:
        return [self.map_text, self.map_text3, self.map_text4]
