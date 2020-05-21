import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *
# https://pysdl2.readthedocs.io/en/rel_0_9_4/modules/sdl2ext_sprite.html
class Sprite(sdl2.ext.Entity):
  def __init__(self, scene, asset, x=128, y=128):
    super(Sprite, self).__init__()
    self.sprite = scene.factory.from_image(RESOURCES.get_path(asset))
    self.sprite.position = (x, y)
    # self.width, self.height = self.sprite.size
    # width, height = self.sprite.size
    # self.sprite.x = width // 2
    # self.sprite.y = height // 2
    # print("WIDTH AND HIGHT")
    # print(width, height)
    # print(self.sprite.x, self.sprite.y)


    # self.sprite.angle = 90
    # self.sprite.angle2 = 90

  def on_update(self, x, y):
    width, height = self.sprite.size
    self.sprite.position = (x - width // 2, y - height // 2)
    # self.sprite.position = (x - self.sprite.x, y - self.sprite.y)
    # self.sprite.position = (x, y)

  def on_draw(self):
    return self.sprite