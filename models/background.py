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

    self.map_tile_y = self.camera.map_tile_y
    self.map_tile_x = self.camera.map_tile_x

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

    self.map_tile_height = len(self.map_data)
    self.map_tile_width = len(self.map_data[0])
    print("self.map_data with size: " + str([self.map_tile_width, self.map_tile_height]))
    for h in range(0, self.map_tile_height):
        for w in range(0, self.map_tile_width):
            self.map_data[h][w]['map_tile'] = MapTile(self.scene, map_data['terrains'][self.map_data[h][w]['terrain_index']], self.tile_height_and_width, w, h)


    # TEST               Y  X
    cell = self.map_data[3][5]['map_tile']
    if cell.map_tile_x != 5:
      print("expected 5, found " + str(cell.map_tile_x))
      raise "CELL DID NOT MATCH X"
    if cell.map_tile_y != 3:
      print("expected 3, found " + str(cell.map_tile_y))
      raise "CELL DID NOT MATCH Y"

    self.map_pixel_width  = round(self.map_tile_height * self.tile_height_and_width)
    self.map_pixel_height = round(self.map_tile_width  * self.tile_height_and_width)


    # print("MAP DATA")
    # print(self.map_data[0][0])
    # {'corner_heights': {'top_left': 3, 'bottom_right': 2.587122972263349, 'bottom_left': 3, 'top_right': 3}, 'terrain_paths_and_weights': {'top_left': {'2': 0.25}, 'bottom_right': {'2': 0.5, '0': 0.5}, 'bottom_left': {'2': 0.25, '0': 0.25}, 'top_right': {'2': 0.25, '0': 0.25}}, 'terrain_index': 2, 'height': 3, 'terrain_type': 'snow'}

    self.visible_map_width  = self.visible_map_tile_width + EXTRA_MAP_TILE_WIDTH
    print("self.visible_map_width: " + str(self.visible_map_width))
    # 12
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
      print("init_visible_map_tiles_matrix ON CENTER TILE: " + str([self.map_tile_x, self.map_tile_y]))
      for h in range(self.map_tile_y - self.visible_map_height_half, self.map_tile_y + self.visible_map_height_half):
          w_counter = 0
          for w in range(self.map_tile_x - self.visible_map_width_half, self.map_tile_x + self.visible_map_width_half):
              # SETTING NONE MAP FOR: [195, 195] ON [0, 0]
              if h >= 0 and h < self.map_tile_height and w >= 0 and w < self.map_tile_width:
                  print("SETTING MAP FOR: " + str([h, w]) + " ON " + str([h_counter, w_counter]))
                  self.visible_map_tiles_matrix[h_counter][w_counter] = self.map_data[h][w]['map_tile']
                  self.visible_map_tiles_matrix[h_counter][w_counter].debug(h_counter, w_counter)
              else:
                print("SETTING NONE MAP FOR: " + str([h, w]) + " ON " + str([h_counter, w_counter]))
                self.visible_map_tiles_matrix[h_counter][w_counter] = None
              w_counter += 1
          h_counter += 1

  def print_visible_map(self):
    row = ""
    print("START")
    for y in range(0, self.visible_map_height):
      for x in range(0, self.visible_map_width):
        cell = self.visible_map_tiles_matrix[y][x]
        if cell:
          row = row + '[' + str(cell.map_tile_x) + ',' + str(cell.map_tile_y) + ']'
        else:
          row = row + '[NA,NA]'
      print(row)
      row = ""
    print("END")

  def refresh_visible_map_tiles_matrix(self):
      map_tile_x_diff = self.map_tile_x - self.camera.map_tile_x

      # map_tile_y_diff = self.map_tile_y - self.camera.map_tile_y

      # # WEST Adds to the left, but not in the right way, cuts bottom
      # if map_tile_x_diff > 0:
      #   print("map_tile_x_diff > 0")
      #   x_offset = self.map_tile_x - self.visible_map_width_half - 1
      #   print("X OFFSET, should be 95 or less: " + str(x_offset))
      #   self.visible_map_tiles_matrix.insert(0, [None for i in range(self.visible_map_width)])
      #   # self.map_tile_width: 120
      #   print("MAP TILE Y: " + str(self.map_tile_y))
      #   for y_offset in range(0, self.visible_map_height):
      #       # x_with_offset = self.map_tile_x + self.visible_map_width_half - w
      #       # x_with_offset = self.map_tile_x + (w - self.visible_map_width_half)
      #       # this is being used on the Y...
      #       y_offset_offset = self.map_tile_y - (y_offset - self.visible_map_height_half)
      #       print("y_offset_offset: " + str(y_offset_offset))
      #       print("INSERTING VISIBLE TIPE: " + str(0) + ',' + str(y_offset) + ' with map: ' + str(x_offset) + ',' + str(y_offset_offset))
      #       # INSERTING VISIBLE TIPE: 0,4 with map: 100,93
      #       self.visible_map_tiles_matrix[0][y_offset] = self.map_data[y_offset_offset][x_offset]['map_tile']
      #       self.visible_map_tiles_matrix[0][y_offset].debug(0, y_offset, True, x_offset, y_offset_offset)

      #       cell = self.visible_map_tiles_matrix[0][y_offset]
      #       if cell.map_tile_x != x_offset:
      #         print("expected " + x_offset + ", found " + str(cell.map_tile_x))
      #         raise "CELL DID NOT MATCH X"
      #       if cell.map_tile_y != y_offset_offset:
      #         print("expected " + y_offset_offset + ", found " + str(cell.map_tile_y))
      #         raise "CELL DID NOT MATCH Y"


      #   # del self.visible_map_tiles_matrix[-1]
      #   self.map_tile_x = self.map_tile_x - 1
      # WEST
      if map_tile_x_diff > 0:
        left_side_x_axis = self.map_tile_x - self.visible_map_width_half - 1
        print("left_side_x_axis: " + str(left_side_x_axis))
        for left_side_y_axis in range(0, self.visible_map_height):
          
          map_data_y_offset = self.map_tile_y + (left_side_y_axis - self.visible_map_height_half)

          cell = self.map_data[map_data_y_offset][left_side_x_axis]['map_tile']

          self.visible_map_tiles_matrix[left_side_y_axis].insert(0, cell)
          # self.visible_map_tiles_matrix[visible_map_y_offset].append(cell)
        self.map_tile_x = self.map_tile_x - 1


        

  def on_draw(self):
    drawable_list = []
    for height_row in self.visible_map_tiles_matrix:
        for tile in height_row:
            if (tile):
                drawable_list.append(tile.on_draw())
    return drawable_list

  def on_update(self):
    # print("BACKGROUND UPDATE")
    self.refresh_visible_map_tiles_matrix()

    h_counter = 0
    for height_row in self.visible_map_tiles_matrix:
      w_counter = 0
      for tile in height_row:
        if (tile):
          tile.on_update(h_counter, w_counter)
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
          for text in cell.on_draw_text():
            drawable_list.append(text.on_draw_text())
    return drawable_list


