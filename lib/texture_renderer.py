import sdl2
import sdl2.ext
from sdl2 import rect, render
from sdl2.ext.compat import isiterable
from lib.constants import *

class TextureRenderer(sdl2.ext.TextureSpriteRenderSystem):
    def __init__(self, target):
        super(TextureRenderer, self).__init__(target)

    def render(self, sprite_element, x=0, y=0):
        """Overrides the render method of sdl2.ext.TextureSpriteRenderSystem to
        use "SDL_RenderCopyEx" instead of "SDL_RenderCopy" to allow sprite
        rotation:
        http://wiki.libsdl.org/SDL_RenderCopyEx
        """
        # r = rect.SDL_Rect(0, 0, 0, 0)
        # texture_sprites = sprites[0]
        # text_sprites    = sprites[1]
        # rcopy = render.SDL_RenderCopyEx
        # renderer = self.sdlrenderer
        # x = x or 0
        # y = y or 0
        # for i in range(Z_ORDER.MAX_DEPTH):
        #     for sprite_element in texture_sprites[i]:
        #         sp = sprite_element.on_draw()
        #         r.x = x + sp.x
        #         r.y = y + sp.y
        #         r.w, r.h = sp.size

        #         # print("DRAW")
        #         # print(type(sprite_element))
        #         # print(type(sp))
        #         r.w = int(r.w / sprite_element.scale)
        #         r.h = int(r.h / sprite_element.scale)
        #         # https://wiki.libsdl.org/SDL_RenderCopyEx
        #         if rcopy(renderer, sp.texture, None, r, sp.angle, None, render.SDL_FLIP_NONE) == -1:
        #             raise SDLError()

        #     for text_element in text_sprites[i]:
        #         self.renderer.copy(text_element.value, dstrect = (text.x, text.y, text.value.size[0], text.value.size[1]))
        r = rect.SDL_Rect(0, 0, 0, 0)
        rcopy = render.SDL_RenderCopyEx
        renderer = self.sdlrenderer
        sp = sprite_element.on_draw()
        r.x = x + sp.x
        r.y = y + sp.y
        r.w = sprite_element.w
        r.h = sprite_element.h
        if rcopy(renderer, sp.texture, None, r, sp.angle, None, render.SDL_FLIP_NONE) == -1:
            raise SDLError()
