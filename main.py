# pipenv shell
# python main.py

import sys
import sdl2.ext

from lib.constants import *
from models.world import World
from models.ball import Ball
from lib.velocity import Velocity
from models.player import Player
from lib.software_renderer import SoftwareRenderer
from lib.movement_system import MovementSystem
from lib.collision_system import CollisionSystem

class MainEngine():

  def __init__(self):
    sdl2.ext.init()

    self.window = sdl2.ext.Window("Hello World!", size=(920, 780))
    

    self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    self.sprite = self.factory.from_image(RESOURCES.get_path("test.png"))
    self.processor = sdl2.ext.TestEventProcessor()
    
    self.world = World()

    spriterenderer = SoftwareRenderer(self.window)

    # factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_paddle1 = self.factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = self.factory.from_color(WHITE, size=(20, 100))

    self.player1 = Player(self.world, sp_paddle1, 0, 250)
    self.player2 = Player(self.world, sp_paddle2, 780, 250)
    sp_ball = self.factory.from_color(WHITE, size=(20, 20))

    movement = MovementSystem(0, 0, 800, 600)
    collision = CollisionSystem(0, 0, 800, 600)

    ball = Ball(self.world, sp_ball, 390, 290)
    ball.velocity.vx = -3000
    collision.ball = ball

    self.world.add_system(movement)
    self.world.add_system(collision)
    self.world.add_system(spriterenderer)


  def main(self):
    self.window.show()
    # Image can't be seen when processor runs 
    # self.processor.run(self.window)
    # spriterenderer = self.factory.create_sprite_render_system(self.window)
    # spriterenderer.render(self.sprite)

    # sdl2.ext.init()
    # window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    # window.show()

    running = True
    while running:
      events = sdl2.ext.get_events()
      for event in events:
        if event.type == sdl2.SDL_QUIT:
          running = False
          break
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_UP:
                self.player1.velocity.vy = -3
            elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                self.player1.velocity.vy = 3
        elif event.type == sdl2.SDL_KEYUP:
            if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                self.player1.velocity.vy = 0

      sdl2.SDL_Delay(10)
      self.world.process()
      # self.window.refresh()

    exit()
    return 0

  def exit(self):
    sdl2.ext.quit()