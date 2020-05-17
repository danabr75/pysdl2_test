import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *

class Player(sdl2.ext.Entity):
  def __init__(self, world, factory, posx=0, posy=0):
    # sdl2.ext.TextureSprite
    # https://pysdl2.readthedocs.io/en/latest/modules/sdl2ext_sprite.html
    # test_sprite = sdl2.ext.TextureSprite()
    # factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=sdl2.ext.Renderer(window))
    # SoftwareSprite vs TextureSprite. can create both?

    # https://pysdl2.readthedocs.io/en/rel_0_9_4/modules/sdl2ext_sprite.html#sdl2.ext.TextureSprite
    sprite = factory.from_image(RESOURCES.get_path("test.png"))
    # sprite = factory.from_text('123', fontmanager=sdl2.ext.FontManager())
    print("GOT HERE")
    print(type(sprite))
    print(sprite)

    # sdl2.ext.sprite.TextureSprite
    # sprite = factory.from_color(WHITE, size=(20, 100))

    self.sprite = sprite
    self.sprite.position = posx, posy
    self.velocity = Velocity(1)
    self.move_left = False
    self.move_right = False
    self.move_up = False
    self.move_down = False
    self.sprite.angle = 90
    self.sprite.angle2 = 90


  def event_update(self, event):
    if event.type == sdl2.SDL_KEYDOWN:
      if event.key.keysym.sym == sdl2.SDLK_w:
        print("PLayer mvoe up")
        self.move_up = True
      if event.key.keysym.sym == sdl2.SDLK_s:
        self.move_down = True
      if event.key.keysym.sym == sdl2.SDLK_d:
        self.move_right = True
      if event.key.keysym.sym == sdl2.SDLK_a:
        self.move_left = True
    elif event.type == sdl2.SDL_KEYUP:
      if event.key.keysym.sym == sdl2.SDLK_w:
        print("PLayer stop mvoe up")
        self.move_up = False
      if event.key.keysym.sym == sdl2.SDLK_s:
        self.move_down = False
      if event.key.keysym.sym == sdl2.SDLK_d:
        self.move_right = False
      if event.key.keysym.sym == sdl2.SDLK_a:
        self.move_left = False