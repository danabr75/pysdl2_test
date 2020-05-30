import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *
from models.sprite import Sprite
import math

class Player(object):

  # def __new__(cls, scene):
  #   player = super().__new__(cls, scene)
  #   player.x = 1
  #   player.y = 1
  #   # player.update_sprite()
  #   return player

  def __init__(self, scene, x=128, y=128):
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
    self.x = x
    self.y = y
    # self.sprite = scene.factory.from_image(RESOURCES.get_path("test.png"))
    self.sprite = Sprite(scene, 'ship.png', self.x, self.y)


    self.velocity = Velocity(1)
    self.move_left = False
    self.move_right = False
    self.move_up = False
    self.move_down = False


    self.controls_enabled = True
    self.rotation_speed = 150
    self.speed = 3
    self.angle = 0

  def rotate_clockwise(self):
    if self.controls_enabled:
      increment = self.rotation_speed #* @fps_scaler
      if self.angle + increment >= MAX_ROTATIONAL_ANGLE:
        self.angle = (self.angle + increment) - MAX_ROTATIONAL_ANGLE
      else:
        self.angle += increment

  def rotate_counterclockwise(self):
    if self.controls_enabled:
      increment = self.rotation_speed# * @fps_scaler
      if self.angle - increment <= 0:
        self.angle = (self.angle - increment) + MAX_ROTATIONAL_ANGLE
      else:
        self.angle -= increment        

  def move_forward(self):
    self.movement(self.speed, self.angle / 100)

  def move_backward(self):
    # pass
    self.movement(self.speed / -3, self.angle / 100)

  def movement(self, speed, angle):
    base_speed = speed #* @height_scale * @fps_scaler
    # print("ANGLE: " + str(angle))
    step = (math.pi/180 * (angle - 90))
    # print("STEP: " + str(step))
    # print("OLD X, OLD Y: " + str([self.x, self.y]))
    # testx = (math.cos(step) * base_speed + self.x)
    # testy = (math.sin(step) * base_speed + self.y)
    self.x = round(math.cos(step) * base_speed + self.x)
    self.y = round(math.sin(step) * base_speed + self.y)
    # print("NEW X, OLD Y: " + str([self.x, self.y]))
    # print("POS X, POS Y: " + str([testx, testy]))


  def on_update(self):
    # self.update_sprite()
    self.sprite.on_update(self.x, self.y, (self.angle / 100))
    # self.sprite.angle
    # pass

  def on_draw(self):
    return [self.sprite.on_draw()]

  # event methods
  def key_status(self, keystatus):
    if keystatus[sdl2.SDL_SCANCODE_W] and keystatus[sdl2.SDL_SCANCODE_S]:
      self.move_up   = False
      self.move_down = False
    elif keystatus[sdl2.SDL_SCANCODE_W]:
      # self.y -= 1
      self.move_forward()
      self.move_up   = True
      self.move_down = False
    elif keystatus[sdl2.SDL_SCANCODE_S]:
      self.move_up   = False
      self.move_down = True
      self.move_backward()
    else:
      self.move_up   = False
      self.move_down = False

    if keystatus[sdl2.SDL_SCANCODE_D] and keystatus[sdl2.SDL_SCANCODE_A]:
      self.move_left  = False
      self.move_right = False
    elif keystatus[sdl2.SDL_SCANCODE_D]:
      self.rotate_clockwise()
      self.move_left  = False
      self.move_right = True
      # self.x += 1
    elif keystatus[sdl2.SDL_SCANCODE_A]:
      self.rotate_counterclockwise()
      self.move_left  = True
      self.move_right = False
      # self.x -= 1
    else:
      self.move_left  = False
      self.move_right = False

  def on_key_press(self, event, sym, mod):
    pass
    # if sym == sdl2.SDLK_w:
    #   # print("PLayer W")
    #   self.y -= 1
    #   # self.x += 1
    #   self.move_up = True
    # if sym == sdl2.SDLK_s:
    #   # print("PLayer S")
    #   self.move_down = True
    #   self.y += 1
    #   # self.x -= 1
    # if sym == sdl2.SDLK_d:
    #   # print("PLayer D")
    #   self.move_right = True
    #   self.x += 1
    # if sym == sdl2.SDLK_a:
    #   # print("PLayer A")
    #   self.move_left = True
    #   self.x -= 1

  def on_key_release(self, event, sym, mod):
    pass
    # if sym == sdl2.SDLK_w:
    #   # print("PLayer stop mvoe up")
    #   self.move_up = False
    # if sym == sdl2.SDLK_s:
    #   self.move_down = False
    # if sym == sdl2.SDLK_d:
    #   self.move_right = False
    # if sym == sdl2.SDLK_a:
    #   self.move_left = False