import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *
from models.sprite import Sprite
from models.text import Text
import math

# import time

class Player(object):
  def __init__(self, scene):
    self.scene = scene
    self.map_tile_x = 100
    self.map_tile_y = 100
    # self.map_x, self.map_y = [None, None]
    self.map_x, self.map_y = self.scene.get_map_x_and_map_y_from_tile(self)
    # print("PLAYER GOT HERE")
    # print(str([self.map_x, self.map_y]))
    # self.x = None
    # self.y = None
    self.x, self.y = [ round(SCREEN_WIDTH // 2), round(SCREEN_HEIGHT // 2) ]
    # self.sprite = scene.factory.from_image(RESOURCES.get_path("test.png"))
    self.sprite = Sprite(scene, 'ship.png', self.x, self.y, Z_ORDER.Player)
    self.h = self.sprite.h
    self.w = self.sprite.w
    self.h_h = round(self.h // 2)
    self.h_w = round(self.w // 2)


    self.velocity = Velocity(1)
    self.move_left = False
    self.move_right = False
    self.move_up = False
    self.move_down = False


    self.controls_enabled = True
    self.rotation_speed = 150
    self.speed = 5
    self.angle = 0

    self.player_text = Text(self.scene, "...", self.x, self.y, Z_ORDER.PlayerUI)
    self.player_text2 = Text(self.scene, "...", self.x, self.y, Z_ORDER.PlayerUI)

    # self.last_update = None
    # self.num_of_updates = 0

  def rotate_clockwise(self):
    if self.controls_enabled:
      increment = self.get_rotation_speed()
      if self.angle + increment >= MAX_ROTATIONAL_ANGLE:
        self.angle = (self.angle + increment) - MAX_ROTATIONAL_ANGLE
      else:
        self.angle += increment

  def rotate_counterclockwise(self):
    if self.controls_enabled:
      increment = self.get_rotation_speed()
      if self.angle - increment <= 0:
        self.angle = (self.angle - increment) + MAX_ROTATIONAL_ANGLE
      else:
        self.angle -= increment        

  def get_rotation_speed(self):
    return round(self.rotation_speed * get_global_fps_modifier())

  def move_forward(self):
    self.movement(self.get_speed(), self.angle / 100)

  def move_backward(self):
    # pass
    self.movement(self.get_speed(-0.3), self.angle / 100)

  def get_speed(self, modifier = None):
    if modifier:
      return self.speed * get_global_fps_modifier() * modifier
    else:
      return self.speed * get_global_fps_modifier()

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
    # # print("PLAYER ON UPDATE: " + str(self.last_update))
    # if self.last_update == None:
    #   self.last_update = time.time()

    # time_diff = int(time.time() - self.last_update)
    # # print("DIFF: " + str(time_diff))
    # # seconds = (time_diff / 60) / 60
    # # print("SECONDS HERE IN DIFF: " + str(seconds))
    # if time_diff >= 10:
    #   print("PLAYER HAD " + str(round(self.num_of_updates / 10)) + " per second")
    #   self.num_of_updates = 0
    #   self.last_update = time.time()
    # else:
    #   self.num_of_updates += 1

    # self.update_sprite()
    # Always center of screen.

    # self.x, self.y = [ round(SCREEN_WIDTH // 2), round(SCREEN_HEIGHT // 2) ]
    self.x, self.y = self.scene.get_x_and_y_pos_from_camera(self)

    # self.h_h = round(self.h // 2)
    # self.h_w = round(self.w // 2)
    # self.x += self.h_w
    # self.y += self.h_h
    self.sprite.on_update(self.x, self.y, round(self.angle // 100.0))
    self.player_text.on_update(self.x, self.y)
    # self.sprite.angle
    # pass

  def occasional_update(self):
    self.map_tile_x, self.map_tile_y = self.scene.get_tile_x_and_tile_y_from_map(self)
    self.player_text  = Text(self.scene, "p tile (" + str(self.map_tile_x) + ", " + str(self.map_tile_y) + ")", self.x, self.y, Z_ORDER.PlayerUI)
    self.player_text2 = Text(self.scene, "p map (" + str(self.map_x) + ", " + str(self.map_y) + ")", self.x, self.y + 30, Z_ORDER.PlayerUI)

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
    pass
    # return [self.player_text, self.player_text2]
