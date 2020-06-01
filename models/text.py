import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *
# https://pysdl2.readthedocs.io/en/rel_0_9_4/modules/sdl2ext_sprite.html
class Text(object):
  def __init__(self, scene, text, x, y, z, font = ARIAL_RED_WHITE):
    self.value = scene.factory.from_text(text, fontmanager = font)
    self.x = x
    self.y = y
    self.z = z

  def on_update(self, x, y):
    self.x = x
    self.y = y

  def on_draw_text(self):
    return self