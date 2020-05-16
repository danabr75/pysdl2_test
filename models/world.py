import sdl2.ext

class World(sdl2.ext.World):
  # 1 is default grav
  # MOVEMENT: 609
  # DEFAULT_DRAG_COEFFICIENT = 5
  # MOVEMENT: 609
  # DEFAULT_DRAG_COEFFICIENT = 1
  # MOVEMENT: 167
  DEFAULT_DRAG_COEFFICIENT = 1
  def __init__(self, drag = DEFAULT_DRAG_COEFFICIENT):
    super(World, self).__init__()
    self.drag = drag