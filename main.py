# pipenv shell
# python main.py


# Simple pygame program

# http://programarcadegames.com/index.php?chapter=example_code


# Import and initialize the pygame library
import pygame
pygame.init()
from lib import z_order
from models.player import Player
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
print(K_w)
print(pygame.K_w)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

block_pos_x = int(SCREEN_WIDTH/2)
block_pos_y = int(SCREEN_HEIGHT/2)
true = True
false = False
move_left = False
move_right = False
move_up = False
move_down = False

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          running = false
        if event.key == pygame.QUIT:
          running = false
        else:
          player.event_update(event)
      elif event.type == KEYUP:
        player.event_update(event)

    # print("x,y:" + str(block_pos_x) + ' and ' + str(block_pos_y))
    # Fill the background with white
    screen.fill((255, 255, 255))

    # surf = pygame.Surface((50, 50))
    # surf.fill((0, 0, 0))
    # rect = surf.get_rect()


    # Draw a solid blue circle in the center
    # pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    # screen.blit(surf, (block_pos_x, block_pos_y))
    player.update()
    player.draw(screen)
    

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()