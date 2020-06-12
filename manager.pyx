# pipenv shell
# python main.py


import os
import platform
from pathlib import Path
print("SDL2 Detection")

root_folder = str(Path(__file__).parents[0])
vendor_folder = str(Path(root_folder + "/vendor_lib"))
if platform.system() == 'Windows':
    if platform.architecture()[0] == '64bit':
        os.environ["PYSDL2_DLL_PATH"] = str(Path(vendor_folder + "/windows/64/grouped_dlls"))
        print(os.getenv("PYSDL2_DLL_PATH"))
        # set PYSDL2_DLL_PATH=str(Path(VENDOR_FOLDER + "/windows/64/grouped_dlls"))
    elif platform.architecture()[0] == '32bit':
        os.environ["PYSDL2_DLL_PATH"] = str(Path(vendor_folder + "/windows/32/grouped_dlls"))
        print(os.getenv("PYSDL2_DLL_PATH"))
        # set PYSDL2_DLL_PATH=str(Path(VENDOR_FOLDER + "/windows/32/grouped_dlls"))
    else:
        raise Exception("INVALID SYSTEM ARCHITECTURE: " + platform.architecture()[0])
else:
    print("Running using local SDL2 libaries")

from lib.constants import *

# WINDOWS INSTALLATION
# Windows requires the DLLs from this src: https://pysdl2.readthedocs.io/en/latest/install.html
# https://www.libsdl.org/projects/SDL_image/
# PySDL2 also offers support for the following SDL-related libraries:
# CAN BE INJECTED INTO C:\Windows\System32, to be picked up.
# SDL2_image (http://www.libsdl.org/projects/SDL_image/)
# SDL2_mixer (http://www.libsdl.org/projects/SDL_mixer/)
# SDL2_ttf (http://www.libsdl.org/projects/SDL_ttf/)
# SDL2_gfx (http://www.ferzkopp.net/Software/SDL_gfx-2.0/)
#
# ALSO NEED SDL2: src: https://www.libsdl.org/download-2.0.php
#   Also injected into C:\Windows\System32
# SDL2-2.0.12-win32-x64
# 
# pyinstaller --add-data="lib;lib" --add-data="models;models" run.py
# dist\run\run.exe
# https://mborgerson.com/creating-an-executable-from-a-python-script/
# ValueError: invalid path 'C:\projects\pysdl2_test-master\dist\run\lib\constants.pyc'


# pyinstaller -F --add-data="lib;lib" --add-data="models;models" run.py
# dist\run.exe
# ValueError: invalid path 'C:\Users\benrd\AppData\Local\Temp\_MEI470202\lib\constants.pyc'


# Add compiled versions of python files. `python -m compileall .` and move them alongside their original files.
# Also had issues with constants.py. Need to fix asset pathing.
#   - Might be fixed
# pyinstaller --windowed --add-data="lib;lib" --add-data="models;models" --add-data="assets;assets" --add-data="maps;maps" --add-data="vendor_lib;vendor_lib" run.py
# dist\run\run.exe

# DEBUG: without windowed
# pyinstaller --add-data="lib;lib" --add-data="models;models" --add-data="assets;assets" --add-data="maps;maps" --add-data="vendor_lib;vendor_lib" run.py
# dist\run\run.exe


import sys
import sdl2
import sdl2.ext

# src: https://github.com/ShadowApex/pysdl2-example/blob/master/physics.py
# import sdl2.sdlgfx
from sdl2 import rect, render
from sdl2.ext.compat import isiterable


import ctypes

from models.world import World
from models.ball import Ball
from lib.velocity import Velocity
# from models.player import Player
# from models.cursor import Cursor
from lib.software_renderer import SoftwareRenderer
# from lib.movement_system import MovementSystem
from lib.collision_system import CollisionSystem
from lib.texture_renderer import TextureRenderer

from models.keyboard_state_controller import KeyboardStateController
from models.scene_base import SceneBase

from lib.clock import Clock
import time

cdef class Manager():
    cpdef void set_scene(self, scene=None):
        # SceneBase self.scene = scene(manager=self)
        self.scene = scene(manager=self)







