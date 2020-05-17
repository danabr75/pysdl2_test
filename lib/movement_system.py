import sdl2.ext
from lib.velocity import Velocity

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
            elif not velocity_y_positive and velocity_y_diff > -1:
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


