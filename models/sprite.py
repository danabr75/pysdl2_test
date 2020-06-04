import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *
# https://pysdl2.readthedocs.io/en/rel_0_9_4/modules/sdl2ext_sprite.html
# Couldn't set scale on entity. Can't add attributes to entities.
# class Sprite(sdl2.ext.Entity):
class Sprite(object):
  def __init__(self, scene, asset, x, y, z, h = None, w = None, scale = DEFAULT_IMAGE_SCALE, always_show = False):
    # super(Sprite, self).__init__()
    # sdl2.ext.Sprite
    self.scale = scale
    self.sprite = scene.factory.from_image(RESOURCES.get_path(asset))
    self.always_show = always_show

    if h:
        self.h = int(h // self.scale)
    else:
        self.h = int(self.sprite.size[1] // self.scale)
    if w:
        self.w = int(w // self.scale)
    else:
        self.w = int(self.sprite.size[0] // self.scale)

    self.h_h = round(self.h // 2)
    self.h_w = round(self.w // 2)

    if x and y:
        self.sprite.position = (x - self.h_w, y - self.h_h)
    # print("HERER")
    # print(self.sprite.frame_rect)
    # self.width, self.height = self.sprite.size
    # width, height = self.sprite.size
    # self.sprite.x = width // 2
    # self.sprite.y = height // 2
    # print("WIDTH AND HIGHT")
    # print(width, height)
    # print(self.sprite.x, self.sprite.y)
    
    self.z = z
    self.sprite.depth = z


  def is_on_screen(self):
    # Need to factor in object width and height.
    if self.always_show:
        return True
    elif self.sprite.y > screen_bottom_with_buffer() and self.sprite.y < get_screen_height_with_buffer() and self.sprite.x > screen_left_with_buffer() and self.sprite.x < get_screen_width_with_buffer():
        return True
    else:
        return False

  # def is_on_screen?
  #   y_buffer = (@screen_pixel_height * 0.2)
  #   x_buffer = (@screen_pixel_width  * 0.2)
  #   @y > -y_buffer && @y < @screen_pixel_height + y_buffer && @x > -x_buffer && @x < @screen_pixel_width + x_buffer
  # end

    # self.sprite.angle = 90
    # self.sprite.angle2 = 90

  def on_update(self, x, y, angle = None):
    width, height = self.sprite.size
    self.sprite.position = (x - 0, y - 0)
    if angle:
        self.sprite.angle = angle
    # self.sprite.position = (x - self.sprite.x, y - self.sprite.y)
    # self.sprite.position = (x, y)

  # should no longer be needed.
  def on_draw(self):
    return self.sprite