from lib.constants import *
import json
from models.map_tile import MapTile
from models.sprite import Sprite

class Background(object):

  def __init__(self, scene, screen_width, screen_height):
    self.scene = scene
    self.camera = self.scene.camera

    self.screen_width  = screen_width
    self.screen_height = screen_height

    self.tile_height_and_width = TILE_WIDTH_AND_HEIGHT
    self.visible_map_tile_width = round(self.screen_width // self.tile_height_and_width)
    print("tile_height_and_width")
    print(self.tile_height_and_width)


    map_file = open(str(Path(MAPS_FOLDER + "/snow.txt")), "r")
    map_data = json.loads(map_file.readline())

    print("MAP TERRAIN")
    print(map_data['terrains'])
    self.terrains = []


    self.map_data = map_data['data']

    self.map_height = len(self.map_data)
    self.map_width = len(self.map_data[0])
    print("self.map_data with size: " + str([self.map_width, self.map_height]))
    for h in range(0, self.map_height):
        for w in range(0, self.map_width):
            self.map_data[h][w]['map_tile'] = MapTile(self.scene, map_data['terrains'][self.map_data[h][w]['terrain_index']], self.tile_height_and_width, h, w)

    self.map_pixel_width  = round(self.map_height  * self.tile_height_and_width)
    self.map_pixel_height = round(self.map_width   * self.tile_height_and_width)


    # print("MAP DATA")
    # print(self.map_data[0][0])
    # {'corner_heights': {'top_left': 3, 'bottom_right': 2.587122972263349, 'bottom_left': 3, 'top_right': 3}, 'terrain_paths_and_weights': {'top_left': {'2': 0.25}, 'bottom_right': {'2': 0.5, '0': 0.5}, 'bottom_left': {'2': 0.25, '0': 0.25}, 'top_right': {'2': 0.25, '0': 0.25}}, 'terrain_index': 2, 'height': 3, 'terrain_type': 'snow'}

    self.visible_map_width  = self.visible_map_tile_width + EXTRA_MAP_TILE_WIDTH
    self.visible_map_width_half = round(self.visible_map_width / 2)
    self.visible_map_height = VISIBLE_MAP_TILE_HEIGHT + EXTRA_MAP_TILE_HEIGHT
    self.visible_map_height_half = round(self.visible_map_height / 2)
    self.visible_map_tiles_matrix = [[None for i in range(self.visible_map_width)] for j in range(self.visible_map_height)]
    self.init_visible_map_tiles_matrix()
    self.texts = []
    # self.sprite = Sprite(scene, 'ship.png', self.x, self.y)
  def init_visible_map_tiles_matrix(self):
      # self.camera.map_x
      # self.camera.map_y
      # for height_row in self.visible_map_tiles_matrix:
      #     for width_element in height_row:
      #         self.visible_map_tiles_matrix
      h_counter = 0
      print("init_visible_map_tiles_matrix ON CENTER TILE: " + str([self.camera.map_tile_x, self.camera.map_tile_y]))
      for h in range(self.camera.map_tile_y - self.visible_map_height_half, self.camera.map_tile_y + self.visible_map_height_half):
          w_counter = 0
          for w in range(self.camera.map_tile_x - self.visible_map_width_half, self.camera.map_tile_x + self.visible_map_width_half):
              # SETTING NONE MAP FOR: [195, 195] ON [0, 0]
              if h >= 0 and h < self.map_height and w >= 0 and w < self.map_width:
                  print("SETTING MAP FOR: " + str([w, h]) + " ON " + str([w_counter, h_counter]))
                  self.visible_map_tiles_matrix[h_counter][w_counter] = self.map_data[h][w]['map_tile']
              else:
                print("SETTING NONE MAP FOR: " + str([w, h]) + " ON " + str([w_counter, h_counter]))
                self.visible_map_tiles_matrix[h_counter][w_counter] = None
              w_counter += 1
          h_counter += 1

  def on_draw(self):
    drawable_list = []
    for height_row in self.visible_map_tiles_matrix:
        for tile in height_row:
            if (tile):
                drawable_list.append(tile.on_draw())
    return drawable_list

  def on_update(self):
    # print("BACKGROUND UPDATE")
    h_counter = 0
    for height_row in self.visible_map_tiles_matrix:
      w_counter = 0
      for tile in height_row:
        if (tile):
          tile.on_update()
            # round((w_counter * self.tile_height_and_width)  - ((EXTRA_MAP_TILE_WIDTH / 2)  * self.tile_height_and_width)),
            # round((h_counter * self.tile_height_and_width) - ((EXTRA_MAP_TILE_HEIGHT / 2) * self.tile_height_and_width))
          # )

        w_counter += 1
      h_counter += 1
      
  def on_draw_text(self):
    drawable_list = []
    for element in self.texts:
      drawable_list.append(element.on_draw_text())
    for height_row in self.visible_map_tiles_matrix:
      for cell in height_row:
        if cell:
          drawable_list.append(cell.on_draw_text())
    return drawable_list


