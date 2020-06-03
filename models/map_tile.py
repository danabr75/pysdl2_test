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
    self.map_text5 = None

  def debug(self, start_visible_map_x, start_visible_map_y, debug_val = False, retrieved_x=None, retrieved_y=None):
    self.debug_val = debug_val
    self.start_visible_map_x = start_visible_map_x
    self.start_visible_map_y = start_visible_map_y
    self.map_text2 = Text(self.scene, "init: " + str(self.start_visible_map_x) + ',' + str(self.start_visible_map_y), 0, 0, Z_ORDER.BackgroundUI)
    if retrieved_x:
        print("RETRIEVED BY: " + str(retrieved_x) + ',' + str(retrieved_y))
        print("VISIBLE BY: " + str(start_visible_map_x) + ',' + str(start_visible_map_y))
        print("FOR MAP TILE: " + str(self.map_tile_x) + ',' + str(self.map_tile_y))
        self.map_text5 = Text(self.scene, "Ret: " + str(retrieved_x) + ',' + str(retrieved_y), 0, 0, Z_ORDER.BackgroundUI)
    if retrieved_x or retrieved_y:
        if retrieved_x != self.map_tile_x:
            print("X DID NOT MATCH: wanted " + str(retrieved_x) + " but got: " + str(self.map_tile_x))
            raise "STOP"
        if retrieved_y != self.map_tile_y:
            print("Y DID NOT MATCH: wanted " + str(retrieved_y) + " but got: " + str(self.map_tile_y))
            raise "STOP"

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
    if self.map_text5:
        self.map_text5.on_update(self.x, self.y + 60)

  def on_draw(self):
    return self.sprite

  def on_draw_text(self):
    if self.map_text2:
        result = [self.map_text, self.map_text2, self.map_text3, self.map_text4]
        if self.map_text5:
            result.append(self.map_text5)
        return result
    else:
        result = [self.map_text, self.map_text3, self.map_text4]
        if self.map_text5:
            result.append(self.map_text5)
        return result
