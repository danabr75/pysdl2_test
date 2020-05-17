# pipenv shell
# python main.py

import sys
import sdl2.ext

from lib.constants import *
from models.world import World
from models.ball import Ball
from lib.velocity import Velocity
from models.player import Player
from models.cursor import Cursor
from lib.software_renderer import SoftwareRenderer
from lib.movement_system import MovementSystem
from lib.collision_system import CollisionSystem

from models.keyboard_state_controller import KeyboardStateController
from models.scene_base import SceneBase

# import os
# from util.time import Clock


class MainEngine():

  def __init__(self, opengl = False):
    sdl2.ext.init()


    if opengl:
        # No hardware accelerated renderers available
        flags = sdl2.SDL_WINDOW_OPENGL
    else:
        flags = sdl2.SDL_RENDERER_SOFTWARE

    # self.window = sdl2.ext.Window("Hello World!", size=(920, 780))
    self.width  = SCREEN_WIDTH
    self.height = SCREEN_HEIGHT

    self.window = sdl2.ext.Window("Tiles", size=(self.width, self.height), flags=flags)
    # self.window = sdl2.ext.Window("Tiles", size=(self.width, self.height), flags=sdl2.SDL_WINDOW_BORDERLESS)

    # Create a renderer that supports hardware-accelerated sprites.
    self.renderer = sdl2.ext.Renderer(self.window)

    # Create a sprite factory that allows us to create visible 2D elements
    # easily.
    self.texture_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)


    # self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    # self.sprite = self.factory.from_image(RESOURCES.get_path("test.png"))
    self.processor = sdl2.ext.TestEventProcessor()
    
    self.world = World()


    # wminfo = SDL_SysWMinfo();
    # SDL_GetVersion(wminfo.version);
    # spriterenderer = SoftwareRenderer(self.window)
    # sdl2.ext.SDL_SetWindowSize(self.window, self.width, self.height)
    sdl2.SDL_SetWindowSize(self.window.window, self.width, self.height)
    spriterenderer = self.texture_factory.create_sprite_render_system(self.window)
 

    # factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    # sp_paddle1 = self.factory.from_color(WHITE, size=(20, 100))

    # cursor_image = self.factory.from_color(GREEN, size=(20, 20))

    # self.cursor = Cursor(self.world, cursor_image)

    self.player1 = Player(self.world, self.texture_factory, 250, 250)
    # self.player2 = Player(self.world, sp_paddle2, 780, 250)
    # sp_ball = self.factory.from_color(WHITE, size=(20, 20))

    movement = MovementSystem(0, 0, 800, 600)
    # collision = CollisionSystem(0, 0, 800, 600)

    # ball = Ball(self.world, sp_ball, 390, 290)
    # ball.velocity.vx = -3000
    # collision.ball = bal

    self.world.add_system(movement)
    # self.world.add_system(collision)
    self.world.add_system(spriterenderer)

    self.event_listeners = {'in_game_state':[self.player1], 'menu': []}
    self.game_states = ['in_game_state', 'menu', 'options']
    self.current_state = self.game_states[0]

    self.width = SCREEN_WIDTH
    self.height = SCREEN_HEIGHT
    self.tile_size = TILE_SIZE
    self.limit_fps = LIMIT_FPS
    self.window_color = WINDOW_COLOR

    # Number of tile_size-sized drawable columns and rows on screen
    self.cols = self.width
    self.rows = self.height

  def main(self):
    self.window.show()
    sdl2.SDL_RaiseWindow(self.window.window)

    # self.kb_state = KeyboardStateController()
    # self._get_mouse_state()
    # self.clock = Clock()

    # Image can't be seen when processor runs 
    # self.processor.run(self.window)

    running = True
    while running:
      events = sdl2.ext.get_events()
      # GAME OPTIONS HERE
      if self.current_state == 'in_game_state':
        for event in events:
          if event.type == sdl2.SDL_QUIT:
            running = False
            break
          if event.type == sdl2.SDL_KEYDOWN:
            if event.key == sdl2.SDLK_ESCAPE:
              # self.current_state = 'menu'
              running = False
          elif event.type == sdl2.SDL_KEYUP:
            if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
              self.player1.velocity.vy = 0
          for listener in self.event_listeners[self.current_state]:
            listener.event_update(event)
      # MENU OPTIONS HERE
      elif self.current_state == 'menu':
        for event in events:
          if event.type == sdl2.SDL_QUIT:
            running = False
            break
          if event.type == sdl2.SDL_KEYDOWN:
            if event.key == sdl2.SDLK_ESCAPE:
              # self.current_state = 'in_game_state'
              running = False
          elif event.type == sdl2.SDL_KEYUP:
            if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
              self.player1.velocity.vy = 0
          for listener in self.event_listeners[self.current_state]:
            listener.event_update(event)
      # self.cursor.update()
      # sdl2.SDL_Delay(10)
      self.world.process()
      # self.window.refresh()
    print('EXIT ME')
    self.exit()
    return sdl2.ext.quit()

  def exit(self):
    sdl2.ext.quit()
    return sdl2.ext.quit()