import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *
from models.sprite import Sprite
from models.text import Text
import math

class Player(object):
  def __init__(self, scene):
    self.scene = scene
    self.map_tile_x = 100
    self.map_tile_y = 100
    # self.map_x, self.map_y = [None, None]
    self.map_x, self.map_y = self.scene.get_map_x_and_map_y_from_tile(self)
    print("PLAYER GOT HERE")
    print(str([self.map_x, self.map_y]))
    self.x = None
    self.y = None
    # self.sprite = scene.factory.from_image(RESOURCES.get_path("test.png"))
    self.sprite = Sprite(scene, 'ship.png', self.x, self.y, Z_ORDER.Player)


    self.velocity = Velocity(1)
    self.move_left = False
    self.move_right = False
    self.move_up = False
    self.move_down = False


    self.controls_enabled = True
    self.rotation_speed = 150
    self.speed = 3
    self.angle = 0

    self.player_text = Text(scene, "player", self.x, self.y, Z_ORDER.PlayerUI)

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
    self.map_x = round(math.cos(step) * base_speed + self.map_x)
    self.map_y = round(math.sin(step) * base_speed + self.map_y)
    # print("NEW X, OLD Y: " + str([self.x, self.y]))
    # print("POS X, POS Y: " + str([testx, testy]))


  def on_update(self):
    # self.update_sprite()
    # Always center of screen.
    self.x, self.y = [ round(SCREEN_WIDTH // 2), round(SCREEN_HEIGHT // 2) ] #self.scene.get_x_and_y_pos_from_camera(self)
    self.sprite.on_update(self.x, self.y, (self.angle / 100))
    self.player_text.on_update(self.x, self.y)
    # self.sprite.angle
    # pass

  def on_draw(self):
    return [self.sprite]

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
  def on_key_release(self, event, sym, mod):
    pass

  def on_draw_text(self):
    return [self.player_text]
