from lib.constants import *

class CameraPOV(object):

  def __init__(self, object, x = None, y = None):
    self.object = object
    if self.object:
      self.x = self.object,x
      self.y = self.object.y
    else:
      self.x = x
      self.y = y
    self.switching_to_other_object = None
    self.map_x = 100
    self.map_y = 100

  def on_update(self):
    self.x = self.object.x
    self.y = self.object.y