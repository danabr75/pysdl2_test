import ctypes
import sdl2.ext
from lib.constants import *
from models.sprite import Sprite

# For testing.
from pymunk.vec2d import Vec2d

class Cursor(object):
  def __init__(self, scene):
    # Show Hide Cursor
    sdl2.SDL_ShowCursor(sdl2.SDL_DISABLE);
    super(Cursor, self).__init__()
    self.is_clicked = False
    self.x, self.y = self._get_mouse_state()

    self.h = round(100 * HEIGHT_SCALER)
    self.w = round(100 * HEIGHT_SCALER)

    self.h_h = round(self.h // 2)
    self.h_w = round(self.w // 2)

    self.unclicked_sprite = Sprite(scene, 'cursor.png', self.x, self.y, Z_ORDER.Cursor, self.w, self.h)
    self.clicked_sprite = Sprite(scene, 'cursor_clicked.png', self.x, self.y, Z_ORDER.Cursor, self.w, self.h)
    self.sprite = self.unclicked_sprite

    self.scene = scene

    self.map_x, self.map_y = self.scene.get_map_x_and_map_y_from_x_and_y(self)
    self.mass = 200
    # self.body = self.scene.add_box(self.map_x, self.map_y, self.w, self.h, self.mass, COLLISION_SHIP_LEVEL)
    self.shape = self.scene.add_box(self.map_x, self.map_y, self.w, self.h, self.mass, COLLISION_SHIP_LEVEL)
    self.body = self.shape.body
    self.x_force = 0




  def on_mouse_drag(self, event, x, y, dx, dy, button):
      # self.sprite.position = (x, y)
      # self.map_x, self.map_y = self.scene.get_map_x_and_map_y_from_x_and_y(self)
      # self.body.position = Vec2d(self.map_x, self.map_y)
      # print("MOUSEE BODU  POSITION")
      # print(str(self.body.position))
      # print("MOUSE MAP POS")
      # print(str([self.map_x, self.map_y]))
      self.unclicked_sprite.on_update(x, y)
      self.clicked_sprite.on_update(x, y)
      self.x = x
      self.y = y

  def on_mouse_motion(self, event, x, y, dx, dy):
      # self.sprite.position = (x, y)
      self.unclicked_sprite.on_update(x, y)
      self.clicked_sprite.on_update(x, y)
      self.x = x
      self.y = y

  def on_mouse_press(self, event, x, y, button, double):
      # print("on_mouse_press")
      if self.is_clicked == False:
          # print("PRESS TRIGGERED AT: " + str([x, y]))
          self.is_clicked = True
          # print(self.is_clicked)
          self.sprite = self.clicked_sprite
          # self.scene.background.print_visible_map()
          self.x_force = 5000

  def on_mouse_release(self, event, x, y, button, double):
      # print("on_mouse_release")
      # print(self.is_clicked)
      if self.is_clicked == True:
          self.is_clicked = False
          # print("SETTING NEW SPRITE")
          self.sprite = self.unclicked_sprite
          self.x_force = 0

  def on_update(self):
    # pass
    # print("mouse x and y: ")
    # print(str([self.x, self.y]))
    self.map_x, self.map_y = self.scene.get_map_x_and_map_y_from_x_and_y(self)
    # print("self.scene.get_map_x_and_map_y_from_x_and_y")
    # print(str([self.map_x, self.map_y]))
    self.body.position = Vec2d(self.map_x, self.map_y)

    if self.x_force != 0:
      self.scene.player.body.apply_force_at_local_point((self.x_force, 0), (self.map_x - self.scene.player.body.position[0], self.map_y - self.scene.player.body.position[1]))
    # print("MOUSEE BODU  POSITION")
    # print(str(self.body.position))

  def on_draw(self):
    return [self.sprite]

  def _get_mouse_state(self):
      """Get the mouse state.

      This is only required during initialization. Later on the mouse
      position will be passed through events.
      """
      # This is an example of what PySDL2, below the hood, does for us.
      # Here we create a ctypes int (i.e. a C type int)
      x = ctypes.c_int(0)
      y = ctypes.c_int(0)
      # And pass it by reference to the SDL C function (i.e. pointers)
      sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
      # The variables were modified by SDL, but are still of C type
      # So we need to get their values as python integers
      _mouse_x = x.value
      _mouse_y = y.value
      # Now we hope we're never going to deal with this kind of stuff again
      return _mouse_x, _mouse_y


