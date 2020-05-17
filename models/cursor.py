import ctypes
import sdl2.ext

class Cursor(sdl2.ext.Entity):
  def __init__(self, world, sprite):
    # super(Cursor, self).__init__()
    # self.unclicked_surf = pygame.Surface((25, 25))
    # self.unclicked_surf.fill((0, 125, 255))
    # self.clicked_surf = pygame.Surface((25, 25))
    # self.clicked_surf.fill((100, 125, 0))
    # self.active_surf = self.unclicked_surf
    self.is_clicked = False
    self.click_held = False
    _mouse_x, _mouse_y = self._get_mouse_state()
    self.x = _mouse_x
    self.y = _mouse_y
    self.sprite = sprite
    self.sprite.position = _mouse_x, _mouse_y


  def event_update(self, event):
    # return True
    # if event.type == MOUSEBUTTONDOWN:
    #   print("CLICKED")
    #   self.is_clicked = True
    #   self.click_held = True
    #   # call clicked on object at cooards?
    # elif event.type == MOUSEBUTTONUP:
    #   self.click_held = False

    # on_mouse_motion, on_mouse_drag
    if event.type == sdl2.SDL_MOUSEMOTION:
      self.x = event.motion.x
      self.y = event.motion.y
      self.sprite.position = event.motion.x, event.motion.y
    #     # x = event.motion.x
    #     # y = event.motion.y
    #     # buttons = event.motion.state
    #     # self._mouse_x = x
    #     # self._mouse_y = y
    #     # dx = self.x - self._mouse_x
    #     # dy = self.y - self._mouse_y
    #     # if buttons & sdl2.SDL_BUTTON_LMASK:
    #     #     scene.on_mouse_drag(event, x, y, dx, dy, "LEFT")
    #     # elif buttons & sdl2.SDL_BUTTON_MMASK:
    #     #     scene.on_mouse_drag(event, x, y, dx, dy, "MIDDLE")
    #     # elif buttons & sdl2.SDL_BUTTON_RMASK:
    #     #     scene.on_mouse_drag(event, x, y, dx, dy, "RIGHT")
    #     # else:
    #     #     scene.on_mouse_motion(event, x, y, dx, dy)
    # # on_mouse_press
    # elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
    # #     x = event.button.x
    # #     y = event.button.y

    # #     button_n = event.button.button
    # #     if button_n == sdl2.SDL_BUTTON_LEFT:
    # #         button = "LEFT"
    # #     elif button_n == sdl2.SDL_BUTTON_RIGHT:
    # #         button = "RIGHT"
    # #     elif button_n == sdl2.SDL_BUTTON_MIDDLE:
    # #         button = "MIDDLE"

    # #     double = bool(event.button.clicks - 1)

    # #     scene.on_mouse_press(event, x, y, button, double)
    # # # on_mouse_scroll (wheel)
    # elif event.type == sdl2.SDL_MOUSEWHEEL:
    #     # offset_x = event.wheel.x
    #     # offset_y = event.wheel.y
    #     # scene.on_mouse_scroll(event, offset_x, offset_y)

    # self.x = x
    # self.y = y






  def update(self):
    return True
    # self.sprite.position = self._get_mouse_state()
    # pass
    # # self.is_clicked = False
    # # if self.click_held:
    # #   self.active_surf = self.clicked_surf
    # # else:
    # #   self.active_surf = self.unclicked_surf


    # x, y = ctypes.c_int(0), ctypes.c_int(0) # Create two ctypes values
    # # Pass x and y as references (pointers) to SDL_GetMouseState()
    # buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
    # # Print x and y as "native" ctypes values
    # # print("GOT HERE")
    # # print(x, y)


  # def draw(self, screen):
  #   screen.blit(self.active_surf, pygame.mouse.get_pos())

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


