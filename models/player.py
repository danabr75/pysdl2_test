import sdl2.ext
from lib.velocity import Velocity
from lib.constants import *
from models.sprite import Sprite
from models.text import Text
import math

# import time
# For testing.
from pymunk.vec2d import Vec2d

class Player(object):

  MASS = 50

  def __init__(self, scene, map_tile_x = None, map_tile_y = None):
    self.scene = scene

    self.map_tile_x = map_tile_x or 100
    self.map_tile_y = map_tile_y or 100
    # self.map_x, self.map_y = [None, None]
    map_x, map_y = self.scene.get_map_x_and_map_y_from_tile(self)
    # print("PLAYER GOT HERE")
    # print(str([self.map_x, self.map_y]))
    # self.x = None
    # self.y = None
    x, y = [ round(SCREEN_WIDTH // 2), round(SCREEN_HEIGHT // 2) ]
    # self.sprite = scene.factory.from_image(RESOURCES.get_path("test.png"))
    self.sprite = Sprite(scene, 'ship.png', x, y, Z_ORDER.Player)
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


    self.engine_speed_increase = 0.2
    self.engine_current_speed  = 0
    self.engine_speed_maximum  = 5 # Which is also the momentum maximum
    self.maximum_momentum  = 100 # Which is also the momentum maximum


    # self.angle = 0

    # self.player_text = Text(self.scene, "...", self.x, self.y, Z_ORDER.PlayerUI)
    # self.player_text2 = Text(self.scene, "...", self.x, self.y, Z_ORDER.PlayerUI)


    self.momentum_angles = {}

    # self.body = self.scene.add_box(self.map_x, self.map_y, self.w, self.h, self.mass, COLLISION_SHIP_LEVEL)
    print("PLAYER BOX")
    self.shape = self.scene.add_box(map_x, map_y, self.w, self.h, self.MASS, COLLISION_SHIP_LEVEL)
    self.body = self.shape.body
    self.forward_force = 0
    self.top_x_force = 0
    self.bottom_x_force = 0

    # self.body = self.scene.pymunk.Body(1,moment=66)
    # self.shapes = [ self.scene.pymunk.Circle(body=self.body, radius=self.h_w) ]
    # self.shapes[0].elasticity = .85
    # self.shapes[0].friction - 0.5
    # self.body.velocity = 0, 0
    # self.body.position = Vec2d(
    #   self.map_x, 
    #   self.map_y
    # )

    # self.map_x, self.map_y

    # self.last_update = None
    # self.num_of_updates = 0

  def rotate_clockwise(self):
    pass
    # if self.controls_enabled:
    #   increment = self.get_rotation_speed()
    #   if self.angle + increment >= MAX_ROTATIONAL_ANGLE:
    #     self.angle = (self.angle + increment) - MAX_ROTATIONAL_ANGLE
    #   else:
    #     self.angle += increment
    #   self.body.angle = self.angle / 100

  def rotate_counterclockwise(self):
    pass
    # if self.controls_enabled:
    #   increment = self.get_rotation_speed()
    #   if self.angle - increment <= 0:
    #     self.angle = (self.angle - increment) + MAX_ROTATIONAL_ANGLE
    #   else:
    #     self.angle -= increment        
    #   self.body.angle = self.angle / 100

  def get_rotation_speed(self):
    return round(self.rotation_speed * get_global_fps_modifier())

  def accelerate(self):
    pass
    print("ACCELLERATE")
    # self.shape.body.apply_force_at_local_point((0, 4000), (self.map_x, self.map_y))
    # https://chipmunk-physics.net/forum/viewtopic.php?t=4666


    # self.shape.body.apply_force_at_local_point((0, -4000), (0, 0))


    # dv = Vec2d(1.2 * self.angle, 0.0)
    # self.body.velocity = self.body.rotation_vector.cpvrotate(dv)

    # self.movement(self.get_speed(), self.angle / 100)
    # print("ACCELERATE: " + str(self.engine_current_speed))
    # self.engine_current_speed += self.engine_speed_increase
    # if self.engine_current_speed > self.engine_speed_maximum:
    #   self.engine_current_speed = self.engine_speed_maximum

    # angle_key = str(self.angle // 100)
    # self.momentum_angles[angle_key] = self.engine_current_speed #// self.mass

    # # if angle_key in self.momentum_angles:
    # #   self.momentum_angles[angle_key] += self.engine_current_speed // self.mass
    # # else:
    # #   self.momentum_angles[angle_key]  = self.engine_current_speed // self.mass

    # if self.momentum_angles[angle_key] > self.maximum_momentum:
    #   self.momentum_angles[angle_key] = self.maximum_momentum

  # DRAG = 1
  # DRAG_MOD = 0.95
  # MOMENTUM_TO_MAP_PIXEL_MOD = 0.1
  # def apply_momentum(self):
  #   for angle in list(self.momentum_angles):
  #     current_momentum = self.momentum_angles[angle]
  #     print("ANGLE: " + str(angle) + ", for momentum: " + str(current_momentum) + " = speed: " + str(int(current_momentum * self.MOMENTUM_TO_MAP_PIXEL_MOD)))
  #     self.movement(int(current_momentum * self.MOMENTUM_TO_MAP_PIXEL_MOD), int(angle))

  #     if current_momentum < self.DRAG:
  #       self.momentum_angles[angle] = (self.momentum_angles[angle] * self.DRAG_MOD) - self.DRAG
  #       print("DELETING ANGLE 1")
  #       del self.momentum_angles[angle]
  #     else:
  #       self.momentum_angles[angle] = (self.momentum_angles[angle] * self.DRAG_MOD) - self.DRAG
  #       if self.momentum_angles[angle] <= 0:
  #         print("DELETING ANGLE 2")
  #         del self.momentum_angles[angle]


  def move_backward(self):
    pass
    # self.movement(self.get_speed(-0.3), self.angle / 100)

  # return Float
  # def get_speed(self, modifier = None):
  #   if modifier:
  #     return self.engine_speed_increase * get_global_fps_modifier() * modifier
  #   else:
  #     return self.engine_speed_increase * get_global_fps_modifier()

  # def movement(self, speed, angle):
  #   base_speed = speed #* @height_scale * @fps_scaler
  #   # print("ANGLE: " + str(angle))
  #   step = (math.pi/180 * (angle - 90))
  #   # print("STEP: " + str(step))
  #   # print("OLD X, OLD Y: " + str([self.x, self.y]))
  #   # testx = (math.cos(step) * base_speed + self.x)
  #   # testy = (math.sin(step) * base_speed + self.y)
  #   self.map_x = round(math.cos(step) * base_speed + self.map_x)
  #   self.map_y = round(math.sin(step) * base_speed + self.map_y)
  #   # print("NEW X, OLD Y: " + str([self.x, self.y]))
  #   # print("POS X, POS Y: " + str([testx, testy]))

  def get_map_pos(self):
    return self.body.position

  def get_map_tile(self):
    return [self.map_tile_x, self.map_tile_y]

  def on_update(self):
    print("body.velocity")
    print(self.body.velocity)
    print(self.body.velocity.length)
    print("BODY ANGLE")
    print(self.body.angle)
    print("angular_velocity")
    print(self.body.angular_velocity)
    # print("X FORCE")
    # print([self.top_x_force, self.bottom_x_force])

    if self.forward_force != 0:
      base_speed = 10
      # step = (math.pi/180 * (self.body.angle - 90))
      step = (math.pi/180 * ((self.body.angle % 360) - 90 ))
      new_map_x = round(math.cos(step) * base_speed + self.body.position[0])
      new_map_y = round(math.sin(step) * base_speed + self.body.position[1])
      diff_x =  self.body.position[0] - new_map_x
      diff_y =  self.body.position[1] - new_map_y
      # x = math.cos(((self.body.angle % 360) - 90) * math.pi / 180 )
      # y = math.sin(((self.body.angle % 360) - 90) * math.pi / 180 )
      # print("X AND Y HERE")
      # print([x, y])
      p1 = Vec2d(self.body.position)
      print("CURRENT POSITION")
      print(p1)
      print("HEADED TO")
      p0 = Vec2d(new_map_x, new_map_y)
      print(p0)
      print("FOR ANGE: " + str(self.body.angle) + " which is to say: " + str(self.body.angle  % 360))
      force = Vec2d(p0 - p1)
      force_from_pos = Vec2d(p1 - p0)

      print("AND GOT FORCE: ")
      print(force)
      force = force * self.forward_force
      # print("AND GOT FORCE * 10: ")
      # print(force)
      # print("FORCE HERE")
      # print(force)
      # [0.7630730056839626, -0.64631229912206]
      # self.body.apply_force_at_local_point((10, 10), (x, y))
      # self.body.apply_force_at_local_point(force, (diff_x, diff_y))
      self.body.apply_force_at_world_point(force, self.body.position)
      # self.body.apply_force_at_local_point(force, force_from_pos)



    # if self.top_x_force != 0 and self.bottom_x_force != 0:

    #   self.body.apply_force_at_local_point((self.top_x_force,    0), (0, self.h))
    #   # self.body.cpvrotate(Vec2d(0, self.h))

      # if self.top_x_force > 0:
      #   self.body.apply_force_at_local_point((self.top_x_force, 0), (-self.h_w, self.h_h))
      # else:
      #   self.body.apply_force_at_local_point((self.top_x_force, 0), (self.h_w, -self.h_h))

      # self.body.apply_force_at_local_point((self.bottom_x_force, 0), (0, self.h))
    if self.move_right:
      self.body.apply_impulse_at_world_point((-9, 0), (self.body.position[0], self.body.position[1] + self.h_h))
      self.body.apply_impulse_at_world_point((9, 0), (self.body.position[0], self.body.position[1] - self.h_h))
    elif self.move_left:
      print("MOVE LEFT")
      self.body.apply_impulse_at_world_point((9, 0), (self.body.position[0], self.body.position[1] + self.h_h))
      self.body.apply_impulse_at_world_point((-9, 0), (self.body.position[0], self.body.position[1] - self.h_h))

      # p0 = Vec2d(self.body.position)
      # p1 = from_pygame(event.pos, self.screen)
      # impulse = 100 * Vec2d(p0 - p1).rotated(-self.body.angle)
      # b.apply_impulse_at_local_point(impulse)

      # self.body.apply_force_at_local_point((10, 0), (0, 30))
    else:
      self.angle_brake()


    # http://www.pymunk.org/en/latest/overview.html
    x, y = self.scene.get_x_and_y_pos_from_camera(self.body.position[0], self.body.position[1])
    self.sprite.on_update(x, y, round(self.body.angle))
    # self.player_text.on_update(self.x, self.y)

  def occasional_update(self):
    self.map_tile_x, self.map_tile_y = self.scene.get_tile_x_and_tile_y_from_map(self.body.position[0], self.body.position[1])

  def on_draw(self):
    return [self.sprite]

  BRAKE_MODIFIER = 0.98
  def brake(self):
    l = self.body.velocity.length
    if l > 5:
        self.body.velocity = self.body.velocity * self.BRAKE_MODIFIER
    else:
      self.body.velocity = Vec2d(0.0, 0.0)

  ANGLE_BRAKE_MODIFIER = 0.80
  def angle_brake(self):
    print("BRAKE HERE")
    l = self.body.angular_velocity
    print(l)
    if l > 0.01:
      print("case 1")
      # print(self.body.angular_velocity)
      # self.body.angular_velocity = self.body.angular_velocity * self.ANGLE_BRAKE_MODIFIER
      # print(self.body.angular_velocity)
      # REDUCING WASN'T WORKING!
      self.body.angular_velocity = 0.0
    else:
      print("case 2")
      self.body.angular_velocity = 0.0

    # self.body.angular_velocity = 0

  # event methods
  def key_status(self, keystatus):
    # brake 
    if keystatus[sdl2.SDL_SCANCODE_S]:
      self.brake()
    else:
      if keystatus[sdl2.SDL_SCANCODE_Q]:
        self.body.apply_force_at_world_point((500, 0), self.body.position)
      elif keystatus[sdl2.SDL_SCANCODE_E]:
        self.body.apply_force_at_world_point((-500, 0), self.body.position)

      if keystatus[sdl2.SDL_SCANCODE_W] and keystatus[sdl2.SDL_SCANCODE_X]:
        self.move_up   = False
        self.move_down = False
        self.forward_force = 0
      elif keystatus[sdl2.SDL_SCANCODE_W]:
        # self.y -= 1
        # self.accelerate()
        # self.body.velocity.y = min(self.body.velocity.y, 2)
        # x, y = self.body.position
        # self.body.position = Vec2d(x, y - 5)
        self.move_up   = True
        self.move_down = False
        self.forward_force = 10
      elif keystatus[sdl2.SDL_SCANCODE_X]:
        self.move_up   = False
        self.move_down = True
        # self.move_backward()
        self.forward_force = -3
      else:
        self.move_up   = False
        self.move_down = False
        self.forward_force = 0

    if keystatus[sdl2.SDL_SCANCODE_D] and keystatus[sdl2.SDL_SCANCODE_A]:
      self.move_left  = False
      self.move_right = False
      # self.top_x_force    = 0
      # self.bottom_x_force = 0
    elif keystatus[sdl2.SDL_SCANCODE_D]:
      # self.rotate_clockwise()
      self.move_left  = False
      self.move_right = True
      # self.top_x_force    =  50
      # self.bottom_x_force = -50
      # self.x += 1
    elif keystatus[sdl2.SDL_SCANCODE_A]:
      # self.rotate_counterclockwise()
      self.move_left  = True
      self.move_right = False
      # self.x -= 1
      # self.top_x_force    = -50
      # self.bottom_x_force =  50
    else:
      self.move_left  = False
      self.move_right = False
      # self.top_x_force    = 0
      # self.bottom_x_force = 0

  def on_key_press(self, event, sym, mod):
    pass
  def on_key_release(self, event, sym, mod):
    pass

  def on_draw_text(self):
    pass
    # return [self.player_text, self.player_text2]
