# pipenv shell
# python main.py


# Simple pygame program

# http://programarcadegames.com/index.php?chapter=example_code


# Import and initialize the pygame library
import pygame
pygame.init()
from lib import z_order
from models.player import Player
from models.cursor import Cursor
# print('test')
# print(z_order.Background)
# print(z_order.Building)

# Set up the drawing window

from OpenGL.GL import *
from OpenGL.GLU import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
    K_w,
    K_a,
    K_s,
    K_d
)
class MainEngine():
  DEFAULT_SCREEN_WIDTH = 800
  DEFAULT_SCREEN_HEIGHT = 600

  def __init__(self):
    self.screen_width  = self.DEFAULT_SCREEN_WIDTH
    self.screen_height = self.DEFAULT_SCREEN_HEIGHT
    # Needs to happen before objects are initted

    pygame.init()
    windowSize = (self.screen_width, self.screen_height)
    self.screen = pygame.display.set_mode(windowSize, pygame.DOUBLEBUF|pygame.OPENGL)
    # void gluPerspective(GLdouble fovy, GLdouble aspect, GLdouble zNear, GLdouble zFar);
    gluPerspective(60, (windowSize[0]/windowSize[1]), 0.1, 100.0)
    # gluOrtho2D(60, (windowSize[0]/windowSize[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -5)
    self.cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
    self.cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1,1,-1))

    # self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    self.player = Player(self.screen_width/2, self.screen_height/2)
    self.cursor = Cursor()
    self.running = True
    pygame.mouse.set_visible(False)
    self.event_listeners = {'in_game_state':[self.player, self.cursor], 'menu': [self.cursor]}
    self.game_states = ['in_game_state', 'menu', 'options']
    self.current_state = self.game_states[0]    

  def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in self.cubeEdges:
      for cubeVertex in cubeEdge:
        glVertex3fv(self.cubeVertices[cubeVertex])
    glEnd()

  def main(self):
    drawable_objects = {}
    drawable_objects[self.player.z] = 'test'
    while self.running:
      if self.current_state == 'in_game_state':
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.running = False
          elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
              self.current_state = 'menu'
            if event.key == pygame.QUIT:
              self.running = false
          for listener in self.event_listeners[self.current_state]:
            listener.event_update(event)
          # map(lambda x: x.event_update(event), event_listeners)
          # cursor.event_update(event)

        # print("x,y:" + str(block_pos_x) + ' and ' + str(block_pos_y))
        # Fill the background with white
        # self.screen.fill((255, 255, 255))

        # # surf = pygame.Surface((50, 50))
        # # surf.fill((0, 0, 0))
        # # rect = surf.get_rect()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


        pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
        self.player.update()
        self.cursor.update()

        self.player.draw(self.screen)
        self.cursor.draw(self.screen)
        glRotatef(1, 1, 1, 1)
        
        glBegin(GL_LINES)
        for cubeEdge in self.cubeEdges:
          for cubeVertex in cubeEdge:
            glVertex3fv(self.cubeVertices[cubeVertex])
            # glVertex2f(self.cubeVertices[cubeVertex])
        glEnd()

        # Flip the display
        pygame.display.flip()
        # pygame.time.wait(10)


      elif self.current_state == 'menu':
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            self.running = False
          elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
              self.current_state = 'in_game_state'
            if event.key == pygame.QUIT:
              self.running = false
          for listener in self.event_listeners[self.current_state]:
            listener.event_update(event)

        # self.screen.fill((255, 255, 255))
        # # UPDATE
        # self.cursor.update()
        # # DRAW
        # self.cursor.draw(self.screen)
        # wireCube()
        # glRotatef(1, 1, 1, 1)
        # glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # glBegin(GL_LINES)
        # for cubeEdge in self.cubeEdges:
        #   for cubeVertex in cubeEdge:
        #     glVertex3fv(cubeVertices[cubeVertex])
        # glEnd()

        # # Flip the display
        # pygame.display.flip()
        # pygame.time.wait(10)
    # END WHILE
    exit()

  def exit(self):
    pygame.quit()

  # Done! Time to quit.
  # pygame.quit()

if __name__ == "__main__":
  MainEngine().main()