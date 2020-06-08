from lib.constants import *

class CameraPOV(object):

  def __init__(self, object, scene, map_x = None, map_y = None):
    self.object = object
    self.scene = scene
    if self.object:
      self.map_x, self.map_y = self.object.get_map_pos()
      self.map_tile_x, self.map_tile_y = self.object.get_map_tile()
    else:
      self.map_x = map_x
      self.map_y = map_y
    self.switching_to_other_object = None

  def on_update(self):
    self.map_x, self.map_y = self.object.get_map_pos()
    # occasional_update ?
    self.map_tile_x, self.map_tile_y = self.object.get_map_tile()

  # def occasional_update(self)
  #   self.map_tile_x = self.object.map_tile_x
  #   self.map_tile_y = self.object.map_tile_y