import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *

class Sprite(sdl2.ext.Entity):
  def __init__(self, scene, asset, x=128, y=128):
    super(Sprite, self).__init__()
    self.sprite = scene.factory.from_image(RESOURCES.get_path(asset))
    self.sprite.position = (x, y)

    # self.sprite.angle = 90
    # self.sprite.angle2 = 90

  def on_update(self, x, y):
    self.sprite.position = (x, y)

  def on_draw(self):
    return self.sprite