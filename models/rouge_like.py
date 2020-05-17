from models.scene_base import SceneBase
import sdl2
import sdl2.ext
from lib.constants import *

class RogueLike(SceneBase):
    """An aspiring Roguelike game's scene."""
 
    def __init__(self, **kwargs):
        """Initialization."""
        # Nothing there for us but lets call super in case we implement
        # something later on, ok?
        super().__init__(**kwargs)
 
        # pass the name of the resource to the sdl2.ext.Resources instance on
        # manager.py
        fname = RESOURCES.get_path("HalfOgreFighter3.png")
 
        # use the pysdl2 factory to create a sprite from an image
        self.sprite = self.factory.from_image(fname)
 
        # set it to a position to look better on our screenshot :)
        self.sprite.position = (128, 128)
 
    def on_update(self):
        """Graphical logic."""
        # use the render method from manager's spriterenderer
        self.manager.spriterenderer.render(sprites=self.sprite)