import sdl2.ext
from sdl2.ext import Color

from pathlib import Path
import os

from lib.z_order import ZOrder


# os.getcwd()
# could replace __file__
Z_ORDER = ZOrder

# in windows, this was still under lib, had to move assets under lib...
#   now fixed with the following.
ROOT_FOLDER = str(Path(__file__).parents[1])
ASSETS_FOLDER = str(Path(ROOT_FOLDER + "/assets"))
VENDOR_FOLDER = str(Path(ROOT_FOLDER + "/vendor_lib"))
MAPS_FOLDER = str(Path(ROOT_FOLDER + "/maps"))
# print( Path(os.getcwd() + "/../assets") )

WHITE = sdl2.ext.Color(255, 255, 255)
GREEN = sdl2.ext.Color(0, 255, 0)
# RESOURCES = sdl2.ext.Resources(__file__, "../assets" )
# RESOURCES = sdl2.ext.Resources(__file__, "..\\assets"  Path(__file__).parents[1] )
RESOURCES = sdl2.ext.Resources(ASSETS_FOLDER)


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


LIMIT_FPS = 60
WINDOW_COLOR = (0, 0, 0, 255)

MAX_ROTATIONAL_ANGLE = 36000

DEFAULT_IMAGE_SCALE = 3

HEIGHT_SCALER = 1.0

# BACKGROUND
# VISIBLE_MAP_TILE_WIDTH  = 6
VISIBLE_MAP_TILE_HEIGHT = 4
# NEED TO BE EVEN NUMBERS
EXTRA_MAP_TILE_HEIGHT   = 8
EXTRA_MAP_TILE_WIDTH    = 12

ARIAL_FONT_WHITE = sdl2.ext.FontManager(font_path = RESOURCES.get_path("arial.ttf"), size = 14)

ARIAL_RED_WHITE  = sdl2.ext.FontManager(font_path = RESOURCES.get_path("arial.ttf"), size = 14, color = Color(255, 0, 0))

TILE_WIDTH_AND_HEIGHT = round(SCREEN_HEIGHT // VISIBLE_MAP_TILE_HEIGHT)

COLLISION_SHIP_LEVEL = 0

global global_fps_modifier
global_fps_modifier = 1

def get_global_fps_modifier():
  global global_fps_modifier
  return global_fps_modifier

def set_global_fps_modifier(value):
  global global_fps_modifier
  global_fps_modifier = value
  return global_fps_modifier
  
global screen_height
global screen_width
screen_height = None
screen_width = None

global screen_height_with_buffer
global screen_bottom_with_buffer
global screen_width_with_buffer
global screen_left_with_buffer

screen_height_with_buffer = None
screen_bottom_with_buffer = None
screen_width_with_buffer = None
screen_left_with_buffer = None

def get_screen_height():
  global screen_height
  return screen_height

def get_screen_width():
  global screen_width
  return screen_width

def get_screen_height_with_buffer():
  global screen_height_with_buffer
  return screen_height_with_buffer

def get_screen_width_with_buffer():
  global screen_width_with_buffer
  return screen_width_with_buffer

def screen_bottom_with_buffer():
  global screen_bottom_with_buffer
  return screen_bottom_with_buffer

def screen_left_with_buffer():
  global screen_left_with_buffer
  return screen_left_with_buffer

def set_screen_dimensions(width, height):
  global screen_width
  global screen_height
  global screen_height_with_buffer
  global screen_bottom_with_buffer
  global screen_width_with_buffer
  global screen_left_with_buffer
  screen_width  = width
  screen_height = height
  screen_height_with_buffer = round(width * 1.2)
  screen_bottom_with_buffer = height - screen_height_with_buffer
  screen_width_with_buffer = round(height * 1.2)
  screen_left_with_buffer = width - screen_width_with_buffer


