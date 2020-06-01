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
VISIBLE_MAP_TILE_HEIGHT = 6
EXTRA_MAP_TILE_HEIGHT   = 4
EXTRA_MAP_TILE_WIDTH    = 4

ARIAL_FONT_WHITE = sdl2.ext.FontManager(font_path = RESOURCES.get_path("arial.ttf"), size = 14)

ARIAL_RED_WHITE  = sdl2.ext.FontManager(font_path = RESOURCES.get_path("arial.ttf"), size = 14, color = Color(255, 0, 0))

TILE_WIDTH_AND_HEIGHT = round(SCREEN_HEIGHT // VISIBLE_MAP_TILE_HEIGHT)


