import sdl2
import sdl2.ext
from lib.constants import *

from models.cursor import Cursor
from models.player import Player
from models.camera_pov import CameraPOV
from models.world import World
from models.text import Text
from models.background import Background

import pymunk
# http://www.pymunk.org/en/latest/pymunk.vec2d.html
# http://www.pymunk.org/en/latest/examples.html
from pymunk.vec2d import Vec2d

class SceneBase(sdl2.ext.World):
    """Basic scene of the game.
 
    New Scenes should be subclasses of SceneBase.
    """
 
    def __new__(cls, manager, **kwargs):
        """Create a new instance of a scene.
 
        A reference to the manager is stored before returning the instance.
        This is made preventively because many properties are related to the
        manager.
 
        Args:
            manager (Manager): the running instance of the Manager
        """
        scene = super().__new__(cls)
        scene.manager = manager
        return scene
 
    def __init__(self, **kwargs):
        super().__init__()
        """Initialization."""
        # pass

        # round(self.DEFAULT_FPS / self.limit_fps, 6)
        self.update_tick = round(1 / self.manager.limit_fps, 6)
        # PYMUNK
        self.pymunk = pymunk
        self.space = self.pymunk.Space()
        self.space.iterations = 10
        self.space.sleep_time_threshold = 0.5
        self.static_body = self.space.static_body
        self.space.gravity = 0.0, 0.0

        # fname = RESOURCES.get_path("cursor.png")
        fname = RESOURCES.get_path("cursor.png")
        player = Player(self)
        self.camera = CameraPOV(player, self)
        self.background = Background(self, self.manager.width, self.manager.height)
 
        # use the pysdl2 factory to create a sprite from an image
        self.cursor_sprite = self.factory.from_image(fname)
 
        # set it to a position to look better on our screenshot :)
        self.cursor_sprite.position = (128, 128)

        
        cursor = Cursor(self)

        self.logo_text = Text(self, "TEXT DRAWABLE", 0, 0, Z_ORDER.UI)


        self.drawable_elements  = [player, cursor, self.background]
        self.updatable_elements = [player, cursor, self.camera, self.background]
        self.key_listeners      = [player]
        self.mouse_listeners    = [cursor]
        self.occasional_updatable_elements = [player]

        self.texts = [self.logo_text]
        self.drawable_text_elements  = [player, self.background]

        self.draw_text = False



        # self.background.map_pixel_width  
        # self.background.map_pixel_height
        # EDGES OF MAP
        shape = self.pymunk.Segment(self.static_body, (1,1), (1,self.background.map_pixel_height), 1.0)
        self.space.add(shape)
        shape.elasticity = 1
        shape.friction = 1

        shape = self.pymunk.Segment(self.static_body, (self.background.map_pixel_width  ,1), (self.background.map_pixel_width  ,self.background.map_pixel_height), 1.0)
        self.space.add(shape)
        shape.elasticity = 1
        shape.friction = 1
        
        shape = self.pymunk.Segment(self.static_body, (1,1), (self.background.map_pixel_width  ,1), 1.0)
        self.space.add(shape)
        shape.elasticity = 1
        shape.friction = 1
        
        shape = self.pymunk.Segment(self.static_body, (1,self.background.map_pixel_height), (self.background.map_pixel_width,self.background.map_pixel_height), 1.0)
        self.space.add(shape)
        shape.elasticity = 1
        shape.friction = 1
        # self.print_options = self.pymunk.SpaceDebugDrawOptions()
        self.collider = self.space.add_collision_handler(COLLISION_SHIP_LEVEL, COLLISION_SHIP_LEVEL)
        self.collider.begin = self.collision_detection

    # /Users/primary_user/projects/pygame/pysdl2_test/models/scene_base.py:109:
    #   UserWarning: Function 'test' should return a bool to indicate if the collision should
    #   be processed or not when used as 'begin' or 'pre_solve' collision callback.
    # Can be factored out to it's own class.
    def collision_detection(self, space, arbiter, data):
        print("test")
        return True
 
    # https://github.com/viblo/pymunk/blob/8a7809a2428cd705e3d9582d776fdf0ca037538a/examples/tank.py#L38
    def add_box(self, map_x, map_y, w, h, mass, collision_type):
        # radius = Vec2d(w, h).length

        body = self.pymunk.Body()

        body.position = Vec2d(map_x, map_y)
        # adding * 30 to test
        shape = self.pymunk.Poly.create_box(body, (w, h), 0.0)
        shape.mass = mass
        shape.friction = 0.5
        shape.elasticity = .85
        shape.collision_type = collision_type
        shape.body = body

        self.space.add(body, shape)
        
        # return body
        return shape

    # https://github.com/viblo/pymunk/blob/8a7809a2428cd705e3d9582d776fdf0ca037538a/examples/tank.py#L38
    def update_space(self, dt):
        self.space.step(dt)

    # properties
    @property
    def height(self):
        """Main window height.
 
        Returns:
            Manager.height
        """
        return self.manager.height
 
    @property
    def width(self):
        """Main window width.
 
        Returns:
            Manager.height
        """
        return self.manager.width
 
    @property
    def factory(self):
        """Reference to sdl2.ext.SpriteFactory instance.
 
        Returns:
            Manager.factory
        """
        return self.manager.factory
 
    @property
    def kb_state(self):
        """Reference to KeyboardStateController instance.
 
        Returns:
            Manager.kb_state
        """
        return self.manager.kb_state
 
    @property
    def renderer(self):
        """Reference to sdl2.ext.Renderer instance.
 
        Returns:
            Manager.renderer
 
        """
        return self.manager.renderer
 
    @property
    def sdlrenderer(self):
        """Reference to sdl2.SDL_Renderer instance.
 
        Returns:
            Manager.renderer.sdlrenderer
        """
        return self.manager.renderer.sdlrenderer
 
    @property
    def spriterenderer(self):
        """Reference to sdl2.ext.TextureSpriteRenderSystem instance.
 
        Returns:
            Manager.spriterenderer
        """
        return self.manager.spriterenderer
 
    # other methods
    def quit(self):
        """Stop the manager main loop."""
        self.manager.quit()
 
    # event methods
    def key_status(self, keystatus):
        for element in self.key_listeners:
            element.key_status(keystatus)

    # event methods
    def on_key_press(self, event, sym, mod):
        """Called on keyboard input, when a key is **held down**.
 
        Args:
            event (sdl2.events.SDL_Event): The base event, as passed by SDL2.
                Unless specifically needed, sym and mod should be used
                instead.
            sym (int): Integer representing code of the key pressed. For
                printable keys ``chr(key)`` should return the corresponding
                character.
            mod (KeyboardStateController): the keyboard state for modifiers
                and locks. See :class:KeyboardStateController
        """
        # pass
        # self.player.on_key_press(event, sym, mod)
        for element in self.key_listeners:
            element.on_key_press(event, sym, mod)
 
    def on_key_release(self, event, sym, mod):
        # print("SCENE KEY RELEASE")
        """Called on keyboard input, when a key is **released**.
 
        By default if the Escape key is pressed the manager quits.
        If that behaviour is desired you can call ``super().on_key_release(
        event, sym, mod)`` on a child class.
 
        Args:
            event (sdl2.events.SDL_Event): The base event, as passed by SDL2.
                The other arguments should be used for a higher level
                interaction, unless specifically needed.
            sym (int): Integer representing code of the key pressed. For
                printable keys ``chr(key)`` should return the corresponding
                character.
            mod (KeyboardStateController): the keyboard state for modifiers
                and locks. See :class:KeyboardStateController
        """
        # self.player.on_key_release(event, sym, mod)
        if sym == sdl2.SDLK_ESCAPE:
            # print("QUITTING HERE")
            self.quit()
        else:

            for element in self.key_listeners:
                element.on_key_release(event, sym, mod)

        # print("GOT:")
        # print(sym)
        # print(sdl2.SDLK_ESCAPE)
        # if sym == sdl2.SDLK_ESCAPE:
        #     print("QUITTING HERE")
        #     self.quit()
 
    def on_mouse_drag(self, event, x, y, dx, dy, button):
        """Called when mouse buttons are pressed and the mouse is dragged.
 
        Args:
            event (sdl2.events.SDL_Event): The base event, as passed by SDL2.
                The other arguments should be used for a higher level
                interaction, unless specifically needed.
            x (int): horizontal coordinate, relative to window.
            y (int): vertical coordinate, relative to window.
            dx (int): relative motion in the horizontal direction
            dy (int): relative motion in the vertical direction
            button (str, "RIGHT"|"MIDDLE"|"LEFT"): string representing the
                button pressed.
        """
        # pass
        # self.cursor_sprite.position = (x, y)
        for element in self.mouse_listeners:
            element.on_mouse_drag(event, x, y, dx, dy, button)
 
    def on_mouse_motion(self, event, x, y, dx, dy):
        """Called when the mouse is moved.
 
        Args:
            event (sdl2.events.SDL_Event): The base event, as passed by SDL2.
                The other arguments should be used for a higher level
                interaction, unless specifically needed.
            x (int): horizontal coordinate, relative to window.
            y (int): vertical coordinate, relative to window.
            dx (int): relative motion in the horizontal direction
            dy (int): relative motion in the vertical direction
        """
        # print("ON MOUSE MOTION")
        # print(x,y,dx,dy)

        # self.cursor_sprite.position = (x, y)
        for element in self.mouse_listeners:
            element.on_mouse_motion(event, x, y, dx, dy)
        # pass
 
    def on_mouse_press(self, event, x, y, button, double):
        """Called when mouse buttons are pressed.
 
        Args:
            event (sdl2.events.SDL_Event): The base event, as passed by SDL2.
                The other arguments should be used for a higher level
                interaction, unless specifically needed.
            x (int): horizontal coordinate, relative to window.
            y (int): vertical coordinate, relative to window.
            button (str, "RIGHT"|"MIDDLE"|"LEFT"): string representing the
                button pressed.
            double (bool, True|False): boolean indicating if the click was a
                double click.
        """
        # pass
        for element in self.mouse_listeners:
            element.on_mouse_press(event, x, y, button, double)
 
    def on_mouse_release(self, event, x, y, button, double):
        for element in self.mouse_listeners:
            element.on_mouse_release(event, x, y, button, double)

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled.
 
        Args:
            event (sdl2.events.SDL_Event): The base event, as passed by SDL2.
                The other arguments should be used for a higher level
                interaction, unless specifically needed.
            offset_x (int): the amount scrolled horizontally, positive to the
                right and negative to the left.
            offset_y (int): the amount scrolled vertically, positive away
                from the user and negative toward the user.
        """
        pass
 
    # Only used by cursor, maybe fixed UI objects
    def get_map_x_and_map_y_from_x_and_y(self, object):
        map_x = object.x + self.camera.map_x - SCREEN_WIDTH  // 2
        map_y = object.y + self.camera.map_y - SCREEN_HEIGHT // 2

        return [map_x, map_y]

    def get_x_and_y_pos_from_camera(self, object):
        # x = self.camera.map_x - object.map_x
        # y = self.camera.map_y - object.map_y
        x = object.map_x - self.camera.map_x + SCREEN_WIDTH  // 2
        y = object.map_y - self.camera.map_y + SCREEN_HEIGHT // 2

        return [x, y]

    def get_map_x_and_map_y_from_tile(self, object):
        return [
            # Rounds down
            int(object.map_tile_x * TILE_WIDTH_AND_HEIGHT), 
            int(object.map_tile_y * TILE_WIDTH_AND_HEIGHT)
        ]

    def get_tile_x_and_tile_y_from_map(self, object):
        return [
            # Rounds down
            int(object.map_x // TILE_WIDTH_AND_HEIGHT), 
            int(object.map_y // TILE_WIDTH_AND_HEIGHT)
        ]


    def occasional_update(self):
        for element in self.occasional_updatable_elements:
            element.occasional_update()

    def on_update(self):
        """Graphical logic."""
        # pass
        # self.player.update()
        # self.manager.spriterenderer.render(sprites=self.cursor_sprite)
        # self.manager.spriterenderer.render(sprites=self.player.sprite)
        self.update_space(self.update_tick)
        for element in self.updatable_elements:
            element.on_update()

    def on_draw(self):
        # drawable_list = []
        # for element in self.drawable_elements:
        #     drawable_list = element.on_draw()
        #     if drawable_list:
        #         for inner_element in drawable_list:
        #             if inner_element:
        #                 drawable_list.append(inner_element)
        # return drawable_list
        drawable_list = {}
        for i in range(Z_ORDER.MAX_DEPTH):
            drawable_list[i] = []

        for element in self.drawable_elements:
            for inner_element in element.on_draw():
                drawable_list[inner_element.z].append(inner_element)
        # self.debug_draw()

        if self.draw_text:
            drawable_text_list = {}
            for i in range(Z_ORDER.MAX_DEPTH):
                drawable_text_list[i] = []

            for element in self.texts:
                drawable_text_list[element.z].append(element.on_draw_text())
            for element in self.drawable_text_elements:
                element_drawable_list = element.on_draw_text()
                if element_drawable_list:
                    for inner_element in element_drawable_list:
                        if (inner_element):
                            drawable_text_list[inner_element.z].append(inner_element)


        # return [drawable_list, drawable_text_list]
        if self.draw_text:
            for i in range(Z_ORDER.MAX_DEPTH):
                # for sprite_element in drawable_list[i]:
                #     self.manager.spriterenderer.render(sprite_element = sprite_element)
                for text in drawable_text_list[i]:
                    self.manager.renderer.copy(text.value, dstrect = (text.x, text.y, text.value.size[0], text.value.size[1]))

        self.manager.spriterenderer.render(drawable_list, Z_ORDER.MAX_DEPTH)


    def debug_draw(self, options = {}):
        self.space.debug_draw(self.print_options)
        # pass
        """Debug draw the current state of the space using the supplied drawing 
        options.        
        If you use a graphics backend that is already supported, such as pygame 
        and pyglet, you can use the predefined options in their x_util modules, 
        for example :py:class:`pygame_util.DrawOptions`.
        Its also possible to write your own graphics backend, see 
        :py:class:`SpaceDebugDrawOptions`.
        If you require any advanced or optimized drawing its probably best to 
        not use this function for the drawing since its meant for debugging 
        and quick scripting. 
        :type options: :py:class:`SpaceDebugDrawOptions`
        """
        # if options._use_chipmunk_debug_draw:
        #     h = ffi.new_handle(self)
        #     # we need to hold h until the end of cpSpaceDebugDraw to prevent GC
        #     options._options.data = h
            
        #     with options:
        #         cp.cpSpaceDebugDraw(self._space, options._options)
        # else:
        #     for shape in self.shapes:
        #         options.draw_shape(shape)

    # def on_draw_text(self):
    #     drawable_text_list = []
    #     for element in self.texts:
    #         drawable_list.append(element.on_draw_text())
    #     for element in self.drawable_text_elements:
    #         element_drawable_list = element.on_draw_text()
    #         if element_drawable_list:
    #             for inner_element in element_drawable_list:
    #                 if (inner_element):
    #                     drawable_list.append(inner_element)
    #     return drawable_list
 
