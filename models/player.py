import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *
from models.sprite import Sprite

class Player(object):

  # def __new__(cls, scene):
  #   player = super().__new__(cls, scene)
  #   player.x = 1
  #   player.y = 1
  #   # player.update_sprite()
  #   return player

  def __init__(self, scene, posx=128, posy=128):
    # super(Player, self).__init__()
    # sdl2.ext.TextureSprite
    # https://pysdl2.readthedocs.io/en/latest/modules/sdl2ext_sprite.html
    # test_sprite = sdl2.ext.TextureSprite()
    # factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=sdl2.ext.Renderer(window))
    # SoftwareSprite vs TextureSprite. can create both?

    # https://pysdl2.readthedocs.io/en/rel_0_9_4/modules/sdl2ext_sprite.html#sdl2.ext.TextureSprite
    # sprite = factory.from_text('123', fontmanager=sdl2.ext.FontManager())
    # print("GOT HERE")
    # print(type(sprite))
    # print(sprite)

    # sdl2.ext.sprite.TextureSprite
    # sprite = factory.from_color(WHITE, size=(20, 100))
    self.scene = scene
    # Depth HERE
    # http://pysdl2.readthedocs.org/en/latest/modules/sdl2ext_sprite.html
    # c.depth = -1
    # Entity(world, c, 100, 100)
    self.x = posx
    self.y = posy
    # self.sprite = scene.factory.from_image(RESOURCES.get_path("test.png"))
    self.sprite = Sprite(scene, 'test.png', self.x, self.y)


    self.velocity = Velocity(1)
    self.move_left = False
    self.move_right = False
    self.move_up = False
    self.move_down = False


  def on_update(self):
    # self.update_sprite()
    self.sprite.on_update(self.x, self.y)
    # pass

  def on_draw(self):
    return [self.sprite.on_draw()]

  def on_key_press(self, event, sym, mod):
    if sym == sdl2.SDLK_w:
      print("PLayer mvoe up")
      self.y += 1
      # self.x += 1
      self.move_up = True
    if sym == sdl2.SDLK_s:
      self.move_down = True
      self.y -= 1
      # self.x -= 1
    if sym == sdl2.SDLK_d:
      self.move_right = True
    if sym == sdl2.SDLK_a:
      self.move_left = True

  def on_key_release(self, event, sym, mod):
    if sym == sdl2.SDLK_w:
      print("PLayer stop mvoe up")
      self.move_up = False
    if sym == sdl2.SDLK_s:
      self.move_down = False
    if sym == sdl2.SDLK_d:
      self.move_right = False
    if sym == sdl2.SDLK_a:
      self.move_left = False