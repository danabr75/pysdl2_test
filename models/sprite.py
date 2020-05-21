import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *

class Sprite(sdl2.ext.Entity):
  def __init__(self, scene, asset, posx=128, posy=128):
    self.sprite = scene.factory.from_image(RESOURCES.get_path(asset))