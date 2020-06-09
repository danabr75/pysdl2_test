import pymunk

class Body(pymunk.Body):
  def __init__(self, mass=0, moment=0, body_type=pymunk.Body.DYNAMIC, custom_object=None):
    # super(Body, self).__init__(mass, moment, body_type)
    super().__init__(mass, moment, body_type)
    self.custom_object = custom_object
