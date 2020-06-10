import sdl2.ext
from lib.constants import *
from models.sprite import Sprite

# import time
# For testing.
from pymunk.vec2d import Vec2d
import math

class Box(object):

  MASS = 1

  def __init__(self, scene, map_tile_x, map_tile_y):
    self.scene = scene

    self.map_tile_x = map_tile_x
    self.map_tile_y = map_tile_y
    map_x, map_y = self.scene.get_map_x_and_map_y_from_tile(self)

    self.sprite = Sprite(scene, 'test.png', 0, 0, Z_ORDER.Player)
    self.h = self.sprite.h
    self.w = self.sprite.w
    self.h_h = round(self.h // 2)
    self.h_w = round(self.w // 2)

    self.shape = self.scene.add_box(map_x, map_y, self.w, self.h, self.MASS, COLLISION_SHIP_LEVEL, self, self.scene.limit_velocity_and_no_angle)
    self.body = self.shape.body

    x, y = self.scene.get_x_and_y_pos_from_camera(self.body.position[0], self.body.position[1])
    print("BOX X AND Y")
    print([x, y])
    print("BOX POS")
    print(self.body.position)
    self.sprite.on_update(x, y, round(self.body.angle))

    self.forward_force = 0
    self.top_x_force = 0
    self.bottom_x_force = 0
    self.health = 100

  def is_alive(self):
    self.health > 0

  def take_damage(self, damage):
    self.health -= damage
    if self.health < 0:
      self.health = 0

  def get_map_pos(self):
    return self.body.position

  def get_map_tile(self):
    return [self.map_tile_x, self.map_tile_y]

  def on_update(self):
    # http://www.pymunk.org/en/latest/overview.html
    print("BOX ON UPDATE")
    print(self.body)
    print(self.body.position)
    x, y = self.scene.get_x_and_y_pos_from_camera(self.body.position[0], self.body.position[1])
    self.sprite.on_update(x, y, round(self.body.angle))

  def occasional_update(self):
    self.map_tile_x, self.map_tile_y = self.scene.get_tile_x_and_tile_y_from_map(self.body.position[0], self.body.position[1])

  def on_draw(self):
    if self.is_alive:
      return [self.sprite]
    else:
      return []

  BRAKE_MODIFIER = 0.98
  def brake(self):
    l = self.body.velocity.length
    if l > 5:
        self.body.velocity = self.body.velocity * self.BRAKE_MODIFIER
    else:
      self.body.velocity = Vec2d(0.0, 0.0)

  ANGLE_BRAKE_MODIFIER = 0.5
  def angle_brake(self):
    if self.body.angular_velocity > 0:
      self.body.apply_impulse_at_world_point(( 1, 0), (self.body.position[0], self.body.position[1] + self.h_h))
      self.body.apply_impulse_at_world_point((-1, 0), (self.body.position[0], self.body.position[1] - self.h_h))
      if self.body.angular_velocity < 0:
        self.body.angular_velocity = 0.0
    elif self.body.angular_velocity < 0:
      self.body.apply_impulse_at_world_point((-1, 0), (self.body.position[0], self.body.position[1] + self.h_h))
      self.body.apply_impulse_at_world_point(( 1, 0), (self.body.position[0], self.body.position[1] - self.h_h))
      if self.body.angular_velocity > 0:
        self.body.angular_velocity = 0.0
