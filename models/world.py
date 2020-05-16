import sdl2.ext

class World(sdl2.ext.World):
  # 1 is default grav
  DEFAULT_DRAG_COEFFICIENT = 1
  def __init__(self, drag = DEFAULT_DRAG_COEFFICIENT):
    super(World, self).__init__()
    self.drag = drag