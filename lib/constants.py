import sdl2.ext

from pathlib import Path
import os



# os.getcwd()
# could replace __file__

# in windows, this was still under lib, had to move assets under lib...
#   now fixed with the following.
ROOT_FOLDER = str(Path(__file__).parents[1])
ASSETS_FOLDER = str(Path(ROOT_FOLDER + "/assets"))
VENDOR_FOLDER = str(Path(ROOT_FOLDER + "/vendor_lib"))
# print( Path(os.getcwd() + "/../assets") )

WHITE = sdl2.ext.Color(255, 255, 255)
GREEN = sdl2.ext.Color(0, 255, 0)
# RESOURCES = sdl2.ext.Resources(__file__, "../assets" )
# RESOURCES = sdl2.ext.Resources(__file__, "..\\assets"  Path(__file__).parents[1] )
RESOURCES = sdl2.ext.Resources(ASSETS_FOLDER)

TILE_SIZE = 32
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

LIMIT_FPS = 60
WINDOW_COLOR = (0, 0, 0, 255)

MAX_ROTATIONAL_ANGLE = 36000

DEFAULT_IMAGE_SCALE = 3