
class DroneListener(object):
    def __init__(self):
        pass
    
    def initialize(self, target_elevation, target_x, simulation_length, path:list() = []):
        pass
    
    def update(self, x, y, roll_angle, thrust, roll, rpm_left, rpm_right, pid_params=None):
        pass
    
    def end_simulation(self, args: dict = dict()):
        pass