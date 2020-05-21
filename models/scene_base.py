import sdl2
import sdl2.ext
from lib.constants import *

from models.cursor import Cursor
from models.player import Player
from models.world import World

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

        # fname = RESOURCES.get_path("cursor.png")
        fname = RESOURCES.get_path("cursor.png")
 
        # use the pysdl2 factory to create a sprite from an image
        self.cursor_sprite = self.factory.from_image(fname)
 
        # set it to a position to look better on our screenshot :)
        self.cursor_sprite.position = (128, 128)

        player = Player(self)
        cursor = Cursor(self)
        self.drawable_elements  = [player, cursor]
        self.updatable_elements = [player]
        self.key_listeners      = [player]
        self.mouse_listeners    = [cursor]
 
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
 
    def on_update(self):
        """Graphical logic."""
        # pass
        # self.player.update()
        # self.manager.spriterenderer.render(sprites=self.cursor_sprite)
        # self.manager.spriterenderer.render(sprites=self.player.sprite)
        for element in self.updatable_elements:
            element.on_update()

    def on_draw(self):
        drawable_list = []
        for element in self.drawable_elements:
            for inner_element in element.on_draw():
                drawable_list.append(inner_element)
        return drawable_list



