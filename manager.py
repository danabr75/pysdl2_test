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

class Manager():
    DEFAULT_FPS = 60

    # OPENGL = False, makes it full screen.
    def __init__(
        self, opengl = True, width = None,
        height = None, cols = None, rows = None, 
        tile_size = None, limit_fps = None,
        window_color = None
    ):
        self.width = width or SCREEN_WIDTH
        self.height = height or SCREEN_HEIGHT
        self.limit_fps = 60#limit_fps or LIMIT_FPS
        self.window_color = window_color or WINDOW_COLOR

        if self.limit_fps == self.DEFAULT_FPS:
            # print("self.limit_fps == self.DEFAULT_FPS")
            set_global_fps_modifier(1)
        else:
            # 3 Precision
            # print(str(self.limit_fps))
            # print(str(self.DEFAULT_FPS))
            set_global_fps_modifier(round(self.DEFAULT_FPS / self.limit_fps, 3))
        # global global_fps_modifier
        # global_fps_modifier = fps_modifier
        print("FPS LIMIT: " + str(self.limit_fps) + " with modifier " + str(get_global_fps_modifier()))

        set_screen_dimensions(self.width, self.height)


        # test = get_global_fps_modifier()
        # print("HOT HERE: " + str(test))
        # raise "stop here"

        # Initialize with no scene
        self.scene = None

        self.show_fps = True
        # self.show_fps = False

        if opengl:
            # No hardware accelerated renderers available, on python 3.7
            flags = sdl2.SDL_WINDOW_OPENGL
        else:
            flags = sdl2.SDL_RENDERER_SOFTWARE

        self.window = sdl2.ext.Window("Tiles", size=(self.width, self.height), flags=flags)
        # Create a renderer that supports hardware-accelerated sprites.
        # AKA texture_renderer
        self.renderer = sdl2.ext.Renderer(self.window)
 
        # Create a sprite factory that allows us to create visible 2D elements
        # easily.
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
 
        # self.text = self.factory.from_text("Unisung Softworks",fontmanager= ARIAL_FONT_WHITE)

        # Creates a simple rendering system for the Window. The
        # SpriteRenderSystem can draw Sprite objects on the window.
 
        # By default, every Window is hidden, not shown on the screen right
        # after creation. Thus we need to tell it to be shown now.
        self.window.show()
        # SpriteRenderSystem can draw Sprite objects on the window.
        # TextureSpriteRenderSystem uses SDL_RenderCopy by default, but you can change it to use SDL_RenderCopyEx
        # Using the TextureSpriteRenderSystem drastically increased the framerate.
        # self.spriterenderer = self.factory.create_sprite_render_system(self.window)
        # Switching over to new renderer for sprite rotation.
        self.spriterenderer = TextureRenderer(self.renderer)
        # self.software_renderer = SoftwareRenderer(self.window)
 
        # Enforce window raising just to be sure.
        sdl2.SDL_RaiseWindow(self.window.window)
 
        # Initialize the keyboard state controller.
        # PySDL2/SDL2 shouldn't need this but the basic procedure for getting
        # key mods and locks is not working for me atm.
        # So I've implemented my own controller.
        self.kb_state = KeyboardStateController()
 
        # Initialize a mouse starting position. From here on the manager will
        # be able to work on distances from previous positions.
        self._get_mouse_state()
 
        # Initialize a clock utility to help us control the framerate
        self.clock = Clock()
 
        # Make the Manager alive. This is used on the main loop.
        self.alive = True

    def _get_mouse_state(self):
        """Get the mouse state.
 
        This is only required during initialization. Later on the mouse
        position will be passed through events.
        """
        # This is an example of what PySDL2, below the hood, does for us.
        # Here we create a ctypes int (i.e. a C type int)
        x = ctypes.c_int(0)
        y = ctypes.c_int(0)
        # And pass it by reference to the SDL C function (i.e. pointers)
        sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
        # The variables were modified by SDL, but are still of C type
        # So we need to get their values as python integers
        self._mouse_x = x.value
        self._mouse_y = y.value
        # Now we hope we're never going to deal with this kind of stuff again
        return self._mouse_x, self._mouse_y
 
    def run(self):
        # Calculate our framerate.
        tick = 0
        update_tick = 0
        if self.show_fps:
            time_new = time.time()
            time_old = time.time()
            time_track = []
        """Main loop handling events and updates."""
        while self.alive:
            tick += 1
            if self.show_fps:
                time_elapsed = time_new - time_old
                time_track.append(time_elapsed)
                time_old = time_new
                time_new = time.time()
            self.clock.tick(self.limit_fps)
            self.on_event()
            self.on_update()

            if self.show_fps:
                if len(time_track) == 60:
                    average = sum(time_track) / len(time_track)
                    print("FPS:", int(1/average))
                    time_track = []
            if self.limit_fps == tick:
                tick = 0
                self.occasional_update()

        return sdl2.ext.quit()

    def on_update(self):
        """Update the active scene."""
        if self.alive:
            self.renderer.clear(self.window_color)
            self.scene.on_update()
            self.scene.on_draw()

            # for text in self.scene.on_draw_text():
            #     self.renderer.copy(text.value, dstrect = (text.x, text.y, text.value.size[0], text.value.size[1]))
            # self.spriterenderer.render(sprites = self.scene.on_draw())
            self.renderer.present()
            # Appears to no longer be necessary.
            # sdl2.timer.SDL_Delay(12)

        # if self.alive:
        #     # clear the window with its color
        #     self.renderer.clear(self.window_color)
        #     if self.scene:
        #         # call the active scene's on_update
        #         self.scene.on_update()

        #     self.renderer.copy(self.text, dstrect= (0,0,self.text.size[0],self.text.size[1]))
        #     # present what we have to the screen
        #     self.renderer.present()
        #     # self.window.refresh()
        #     # https://pysdl2.readthedocs.io/en/latest/tutorial/pygamers.html#pygame-time
        #     # SDL_Delay(1000//FPS - ((SDL_GetTicks()-starttime)))
        #     # frameTime = sdl2.timer.SDL_GetTicks() - frameStart;
        #     # if frameDelay > frameTime:
        #     #     sdl2.timer.SDL_Delay(frameDelay - frameTime);
        #     sdl2.timer.SDL_Delay(100)
 
    def occasional_update(self):
        if self.alive:
            self.scene.occasional_update()

    def present(self):
        """Flip the GPU buffer."""
        sdl2.render.SDL_RenderPresent(self.spriterenderer.sdlrenderer)
 
    def set_scene(self, scene=None, **kwargs):
        """Set the scene.
 
        Args:
            scene (SceneBase): the scene to be initialized
            kwargs: the arguments that should be passed to the scene
 
        """
        self.scene = scene(manager=self, **kwargs)

    def quit(self):
      self.alive = False

    def get_keyboard_state(self):
        """ Returns a list with the current SDL keyboard state,
        which is updated on SDL_PumpEvents. """
        numkeys = ctypes.c_int()
        keystate = sdl2.keyboard.SDL_GetKeyboardState(ctypes.byref(numkeys))
        ptr_t = ctypes.POINTER(ctypes.c_uint8 * numkeys.value)        
        return ctypes.cast(keystate, ptr_t)[0]

    def on_event(self):
        """Handle the events and pass them to the active scene."""
        scene = self.scene
 
        if scene is None:
            return

        # events = []
        # for test in sdl2.ext.get_events():
        #     events.append(test.key.keysym.sym)
        # if len(events) > 0:
        #     print("BEING PRESSED")
        #     print(events)

        # events = []
        # test2 = ctypes.c_int(8)
        # for test in sdl2.SDL_GetKeyboardState(test2):
        #     # print(test)
        #     events.append(test)
        # if len(events) > 0:
        #     print("BEING PRESSED")
        #     print(events)
        keystatus = self.get_keyboard_state()
        scene.key_status(keystatus)
        # if keystatus[sdl2.SDL_SCANCODE_W]:
        #   print("the w key was pressed")


        for event in sdl2.ext.get_events():
            # print("EVENT LOOP HERE")
            # Exit events
            if event.type == sdl2.SDL_QUIT:
                self.quit()
                return
 
            # Redraw in case the focus was lost and now regained
            if event.type == sdl2.SDL_WINDOWEVENT_FOCUS_GAINED:
                self.on_update()
                continue
 
            # on_mouse_motion, on_mouse_drag
            if event.type == sdl2.SDL_MOUSEMOTION:
                x = event.motion.x
                y = event.motion.y
                buttons = event.motion.state
                self._mouse_x = x
                self._mouse_y = y
                dx = x - self._mouse_x
                dy = y - self._mouse_y
                if buttons & sdl2.SDL_BUTTON_LMASK:
                    scene.on_mouse_drag(event, x, y, dx, dy, "LEFT")
                elif buttons & sdl2.SDL_BUTTON_MMASK:
                    scene.on_mouse_drag(event, x, y, dx, dy, "MIDDLE")
                elif buttons & sdl2.SDL_BUTTON_RMASK:
                    scene.on_mouse_drag(event, x, y, dx, dy, "RIGHT")
                else:
                    scene.on_mouse_motion(event, x, y, dx, dy)
                continue
            # on_mouse_press
            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                x = event.button.x
                y = event.button.y
 
                button_n = event.button.button
                button = 'UNDEFINED'
                if button_n == sdl2.SDL_BUTTON_LEFT:
                    button = "LEFT"
                elif button_n == sdl2.SDL_BUTTON_RIGHT:
                    button = "RIGHT"
                elif button_n == sdl2.SDL_BUTTON_MIDDLE:
                    button = "MIDDLE"
 
                double = bool(event.button.clicks - 1)
 
                scene.on_mouse_release(event, x, y, button, double)
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x = event.button.x
                y = event.button.y
 
                button_n = event.button.button
                button = 'UNDEFINED'
                if button_n == sdl2.SDL_BUTTON_LEFT:
                    button = "LEFT"
                elif button_n == sdl2.SDL_BUTTON_RIGHT:
                    button = "RIGHT"
                elif button_n == sdl2.SDL_BUTTON_MIDDLE:
                    button = "MIDDLE"
 
                double = bool(event.button.clicks - 1)
 
                scene.on_mouse_press(event, x, y, button, double)
                continue
            # on_mouse_scroll (wheel)
            elif event.type == sdl2.SDL_MOUSEWHEEL:
                offset_x = event.wheel.x
                offset_y = event.wheel.y
                scene.on_mouse_scroll(event, offset_x, offset_y)
                continue
 
            # for keyboard input, set the key symbol and keyboard modifiers
            mod = self.kb_state.process(event)
            sym = event.key.keysym.sym

            # on_key_release
            if event.type == sdl2.SDL_KEYUP:
                # print("TEST")
                scene.on_key_release(event, sym, mod)
            # on_key_press
            elif event.type == sdl2.SDL_KEYDOWN:
                scene.on_key_press(event, sym, mod)
