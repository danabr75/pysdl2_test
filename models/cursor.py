import ctypes
import sdl2.ext
from lib.constants import *

class Cursor(sdl2.ext.Entity):
  def __init__(self, scene):
    super(Cursor, self).__init__()
    self.is_clicked = False
    _mouse_x, _mouse_y = self._get_mouse_state()

    # self.unclicked_sprite = scene.factory.from_image(RESOURCES.get_path("cursor.png"))
    # self.clicked_sprite = scene.factory.from_image(RESOURCES.get_path("cursor_clicked.png"))
    self.sprite = scene.factory.from_image(RESOURCES.get_path("cursor.png"))
    self.sprite.position = _mouse_x, _mouse_y

  def on_mouse_drag(self, event, x, y, dx, dy, button):
      self.sprite.position = (x, y)

  def on_mouse_motion(self, event, x, y, dx, dy):
      self.sprite.position = (x, y)

  def on_mouse_press(self, event, x, y, button, double):
      pass
      if self.is_clicked == False:
          self.is_clicked == True
          self.sprite = self.clicked_sprite

  def on_mouse_release(self, event, x, y, button, double):
      pass
      if self.is_clicked == True:
          self.is_clicked == False
          self.sprite = self.unclicked_sprite

  def on_update(self):
    pass

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


