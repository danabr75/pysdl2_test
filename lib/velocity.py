class Velocity(object):
    def __init__(self, mass, debug = False):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0
        self.mass = mass
        self.debug = debug