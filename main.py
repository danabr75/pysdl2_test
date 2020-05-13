# pipenv shell
# python main.py

# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

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
        keys = pygame.key.get_pressed()
        # print("keys pressed")
        # print(keys)
        # print("KEY DOWN")
        # print(event.type)
        # Was it the Escape key? If so, stop the loop.
        if event.key == K_ESCAPE:
          running = false
        if event.key == pygame.QUIT:
          running = false
        if event.key == K_w:
          move_up = true
        if event.key == K_s:
          move_down = true
        if event.key == K_d:
          move_right = true
        if event.key == K_a:
          move_left = true
      elif event.type == KEYUP:
        if event.key == K_w:
          move_up = false
        if event.key == K_s:
          move_down = false
        if event.key == K_d:
          move_right = false
        if event.key == K_a:
          move_left = false

    if move_left:
      block_pos_x -= 1
    if move_right:
      block_pos_x += 1
    if move_up:
      block_pos_y -= 1
    if move_down:
      block_pos_y += 1

    # print("x,y:" + str(block_pos_x) + ' and ' + str(block_pos_y))
    # Fill the background with white
    screen.fill((255, 255, 255))

    surf = pygame.Surface((50, 50))
    surf.fill((0, 0, 0))
    rect = surf.get_rect()
    screen.blit(surf, (block_pos_x, block_pos_y))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()