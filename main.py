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
    self.screen_width = self.DEFAULT_SCREEN_WIDTH
    self.screen_height = self.DEFAULT_SCREEN_HEIGHT
    self.player = Player(self.screen_width/2, self.screen_height/2)
    self.cursor = Cursor()

    self.running = True
    pygame.mouse.set_visible(False)
    self.event_listeners = {'in_game_state':[self.player, self.cursor], 'menu': [self.cursor]}
    self.game_states = ['in_game_state', 'menu', 'options']
    self.current_state = self.game_states[0]    
    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

  def main(self):
    

    block_pos_x = int(self.screen_width/2)
    block_pos_y = int(self.screen_height/2)
    true = True
    false = False
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    # Run until the user asks to quit

    drawable_objects = {}
    drawable_objects[self.player.z] = 'test'
    while self.running:
        # Did the user click the window close button?


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
        self.screen.fill((255, 255, 255))

        # surf = pygame.Surface((50, 50))
        # surf.fill((0, 0, 0))
        # rect = surf.get_rect()


        # Draw a solid blue circle in the center
        # pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
        # screen.blit(surf, (block_pos_x, block_pos_y))
        self.player.update()
        self.cursor.update()

        self.player.draw(self.screen)
        self.cursor.draw(self.screen)
        

        # Flip the display
        pygame.display.flip()
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

        self.screen.fill((255, 255, 255))
        # UPDATE
        self.cursor.update()
        # DRAW
        self.cursor.draw(self.screen)
        # Flip the display
        pygame.display.flip()
    # END WHILE
    exit()

  def exit(self):
    pygame.quit()

  # Done! Time to quit.
  # pygame.quit()

if __name__ == "__main__":
  MainEngine().main()