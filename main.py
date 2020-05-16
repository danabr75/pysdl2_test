# pipenv shell
# python main.py

import sys
import sdl2.ext

from lib.constants import *
from models.world import World
from models.ball import Ball
from lib.velocity import Velocity

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
  def __init__(self, window):
    super(SoftwareRenderer, self).__init__(window)

  def render(self, components):
    sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
    super(SoftwareRenderer, self).render(components)

class Player(sdl2.ext.Entity):
  def __init__(self, world, sprite, posx=0, posy=0):
    self.sprite = sprite
    self.sprite.position = posx, posy
    self.velocity = Velocity(1)

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
    self.sp_paddle1 = self.factory.from_color(WHITE, size=(20, 100))
    self.sp_paddle2 = self.factory.from_color(WHITE, size=(20, 100))

    self.player1 = Player(self.world, self.sp_paddle1, 0, 250)
    self.player2 = Player(self.world, self.sp_paddle2, 780, 250)
    self.sp_ball = self.factory.from_color(WHITE, size=(20, 20))

    movement = MovementSystem(0, 0, 800, 600)
    collision = CollisionSystem(0, 0, 800, 600)



    self.ball = Ball(self.world, self.sp_ball, 390, 290)
    self.ball.velocity.vx = -3000
    collision.ball = self.ball

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


class MovementSystem(sdl2.ext.Applicator):

    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size

            self.implement_drag(world, velocity)

            sprite.x += round((velocity.vx) / 100)
            sprite.y += round((velocity.vy) / 100)

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight

    def implement_drag(self, world, velocity):
      if world.drag and world.drag >= 1 and velocity.mass > 0:
        # HANDLE Y
        if velocity.vy != 0:
          velocity_y_positive = velocity.vy > 0

          if velocity.vy > 0 and velocity.vy <= 1:
            velocity_y_diff = 0
            velocity.vy = 0
          else:
            velocity_y_diff = round((velocity.vx) / (velocity.mass / world.drag))
            if velocity_y_positive and velocity_y_diff < 1:
              velocity_y_diff = 1
            elif not velocity_x_positive and velocity_y_diff > -1:
              velocity_y_diff = -1


          if (velocity_y_positive and velocity_y_diff < 0) or (not velocity_y_positive and velocity_y_diff > 0):
            velocity_y_diff = 0

          velocity.vy -= velocity_y_diff

        # HANDLE X
        if velocity.vx != 0:
          velocity.movement += 1
          if velocity.debug:
            print("MOVEMENT: " + str(velocity.movement))
          velocity_x_positive = velocity.vx > 0

          if velocity.vx > 0 and velocity.vx <= 1:
            velocity_x_diff = 0
            velocity.vx = 0
          else:
            velocity_x_diff = round((velocity.vx) / (velocity.mass / world.drag))
            if velocity.debug:
              print("velocity_x_diff = round(abs(velocity.vx) / velocity.mass)")
              print(str(velocity_x_diff) + " = round((" + str(velocity.vx) + ") / " + str(velocity.mass) + ")")
              print(str(velocity_x_diff) + " = round(" + str((velocity.vx) / velocity.mass) + ")")
              print('new diff ' + str(velocity_x_diff))


            if velocity_x_positive and velocity_x_diff < 1:
              velocity_x_diff = 1
            elif not velocity_x_positive and velocity_x_diff > -1:
              velocity_x_diff = -1

          if (velocity_x_positive and velocity_x_diff < 0) or (not velocity_x_positive and velocity_x_diff > 0):
            velocity_x_diff = 0

          velocity.vx -= velocity_x_diff



class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def _overlap(self, item):
        pos, sprite = item
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return (bleft < right and bright > left and
                btop < bottom and bbottom > top)

    def process(self, world, componentsets):
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if collitems:
            self.ball.velocity.vx = -self.ball.velocity.vx





if __name__ == "__main__":
  MainEngine().main()