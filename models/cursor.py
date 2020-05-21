import ctypes
import sdl2.ext
from lib.constants import *
from models.sprite import Sprite

class Cursor(object):
  def __init__(self, scene):
    sdl2.SDL_ShowCursor(sdl2.SDL_DISABLE);
    super(Cursor, self).__init__()
    self.is_clicked = False
    _mouse_x, _mouse_y = self._get_mouse_state()

    self.unclicked_sprite = Sprite(scene, 'cursor.png', _mouse_x, _mouse_y)
    self.clicked_sprite = Sprite(scene, 'cursor_clicked.png', _mouse_x, _mouse_y)
    self.sprite = self.unclicked_sprite

  def on_mouse_drag(self, event, x, y, dx, dy, button):
      # self.sprite.position = (x, y)
      self.unclicked_sprite.on_update(x, y)
      self.clicked_sprite.on_update(x, y)

  def on_mouse_motion(self, event, x, y, dx, dy):
      # self.sprite.position = (x, y)
      self.unclicked_sprite.on_update(x, y)
      self.clicked_sprite.on_update(x, y)

  def on_mouse_press(self, event, x, y, button, double):
      print("on_mouse_press")
      if self.is_clicked == False:
          print("PRESS TRIGGERED")
          self.is_clicked = True
          print(self.is_clicked)
          self.sprite = self.clicked_sprite

  def on_mouse_release(self, event, x, y, button, double):
      print("on_mouse_release")
      print(self.is_clicked)
      if self.is_clicked == True:
          self.is_clicked = False
          print("SETTING NEW SPRITE")
          self.sprite = self.unclicked_sprite

  def on_update(self):
    pass

  def on_draw(self):
    return [self.sprite.on_draw()]

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


