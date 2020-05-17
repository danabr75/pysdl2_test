import sdl2
import sdl2.ext


class KeyboardStateController:
    """A class that keeps track of keyboard modifiers and locks."""
 
    def __init__(self):
        """Initialization."""
        self._shift = False
        self._ctrl = False
        self._alt = False
        self.caps = False
        self.num = False
        self.scroll = False
 
    def contains(self, *args):
        """..."""
        d = {arg: True for arg in args}
        return self.combine(**d)
 
    @property
    def alt(self):
        """..."""
        return self.combine(ctrl=True)
 
    @property
    def ctrl(self):
        """..."""
        return self.combine(ctrl=True)
 
    @property
    def shift(self):
        """..."""
        return self.combine(shift=True)
 
    def combine(self, alt=False, ctrl=False, shift=False):
        """..."""
        return all(
            (self._alt == alt,
             self._ctrl == ctrl,
             self._shift == shift)
        )
 
    def process(self, event):
        """Process the current event and update the keyboard state."""
        down = True if event.type == sdl2.SDL_KEYDOWN else False
        self._process_mods(event.key.keysym.sym, down)
        if not down:
            self._process_locks(event.key.keysym.sym)
        return self
 
    def _process_locks(self, key):
        """Process the locks."""
        for lock, sym in (
            ("caps", sdl2.SDLK_CAPSLOCK),
            ("num", sdl2.SDLK_NUMLOCKCLEAR),
            ("scroll", sdl2.SDLK_SCROLLLOCK)
        ):
            if key == sym:
                _prev_lock = getattr(self, lock)
                setattr(self, lock, not _prev_lock)
 
    def _process_mods(self, key, down):
        """Process the modifiers."""
        for mod, syms in (
            ("_ctrl", (sdl2.SDLK_LCTRL, sdl2.SDLK_RCTRL)),
            ("_shift", (sdl2.SDLK_LSHIFT, sdl2.SDLK_RSHIFT)),
            ("_alt", (sdl2.SDLK_LALT, sdl2.SDLK_RALT))
        ):
            if key in syms:
                setattr(self, mod, down)
 
    def __getstate__(self):
        """Prevent pickling."""
        return None
 
    def __repr__(self):
        """Representation of keyboard states."""
        return (
            "alt: %r, ctrl: %r, shift: %r, caps: %r, num: %r, scroll %r" %
            (self.alt, self.ctrl, self.shift, self.caps, self.num,
             self.scroll))