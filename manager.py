# pipenv shell
# python main.py

import sys
import sdl2
import sdl2.ext
import ctypes
import os

from lib.constants import *
from models.world import World
from models.ball import Ball
from lib.velocity import Velocity
from models.player import Player
# from models.cursor import Cursor
from lib.software_renderer import SoftwareRenderer
from lib.movement_system import MovementSystem
from lib.collision_system import CollisionSystem

from models.keyboard_state_controller import KeyboardStateController
from models.scene_base import SceneBase

from lib.clock import Clock


class Manager():

    # OPENGL = False, makes it full screen.
    def __init__(self, opengl = True, width=None, height=None, cols=None, rows=None, tile_size=None,
        limit_fps=None, window_color=None
    ):
        self.width = width or SCREEN_WIDTH
        self.height = height or SCREEN_HEIGHT
        self.tile_size = tile_size or TILE_SIZE
        self.limit_fps = limit_fps or LIMIT_FPS
        self.window_color = window_color or WINDOW_COLOR
 
        # Number of tile_size-sized drawable columns and rows on screen
        self.cols = self.width // self.tile_size
        self.rows = self.height // self.tile_size
 
        # Initialize with no scene
        self.scene = None

        if opengl:
            # No hardware accelerated renderers available, on python 3.7
            flags = sdl2.SDL_WINDOW_OPENGL
        else:
            flags = sdl2.SDL_RENDERER_SOFTWARE

        self.window = sdl2.ext.Window("Tiles", size=(self.width, self.height), flags=flags)

        # Create a renderer that supports hardware-accelerated sprites.
        self.renderer = sdl2.ext.Renderer(self.window)
 
        # Create a sprite factory that allows us to create visible 2D elements
        # easily.
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
 
        # Creates a simple rendering system for the Window. The
        # SpriteRenderSystem can draw Sprite objects on the window.
        self.spriterenderer = self.factory.create_sprite_render_system(self.window)
 
        # By default, every Window is hidden, not shown on the screen right
        # after creation. Thus we need to tell it to be shown now.
        self.window.show()
 
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
        """Main loop handling events and updates."""
        while self.alive:
            self.clock.tick(self.limit_fps)
            self.on_event()
            self.on_update()
        return sdl2.ext.quit()

    def on_update(self):
        """Update the active scene."""
        scene = self.scene
        if self.alive:
            # clear the window with its color
            self.renderer.clear(self.window_color)
            if scene:
                # call the active scene's on_update
                scene.on_update()
            # present what we have to the screen
            self.present()
 
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


    def on_event(self):
        """Handle the events and pass them to the active scene."""
        scene = self.scene
 
        if scene is None:
            return
        for event in sdl2.ext.get_events():
 
            # Exit events
            if event.type == sdl2.SDL_QUIT:
                self.alive = False
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
            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                x = event.button.x
                y = event.button.y
 
                button_n = event.button.button
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
                scene.on_key_release(event, sym, mod)
            # on_key_press
            elif event.type == sdl2.SDL_KEYDOWN:
                scene.on_key_press(event, sym, mod)