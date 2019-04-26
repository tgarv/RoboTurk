class Head:
    def __init__(self):
        # TODO not sure how to initialize the head, since it could end in a place other than (0, 0). Might need to enforce that it gets moved there during shutdown.
        self.position_x = 0.0
        self.position_y = 0.0

    def move_to_position(self, x, y):
        delta_x = x - self.position_x
        delta_y = y - self.position_y
        self.position_x = x
        self.position_y = y
        print("Moving head (%s, %s)" % (delta_x, delta_y))
        # Move motors here

    def set_magnet(self, power):
        # Set magnet's power status to on or off depending on power
        pass