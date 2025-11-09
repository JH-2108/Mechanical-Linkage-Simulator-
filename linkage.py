import numpy as np

class Link:
    """Represents a single bar/link in the mechanism."""
    def __init__(self, name, length, angle_deg=0, fixed=False, angular_velocity=0, type="normal"):
        self.name = name
        self.length = length
        self.angle_deg = angle_deg
        self.fixed = fixed
        self.angular_velocity = angular_velocity
        self.type = type  

class Joint:
    """Represents a joint connecting links."""
    def __init__(self, name, x=0, y=0, connects=None, fixed=False):
        self.name = name
        self.x = x
        self.y = y
        self.connects = connects if connects else []
        self.fixed = fixed

class Linkage:
    """Handles an entire mechanism with multiple links and joints."""
    def __init__(self, links_data, joints_data):
        self.links = [Link(**link) for link in links_data]
        self.joints = [Joint(**joint) for joint in joints_data]

    def update_positions(self, dt):
        """
        Update link angles based on angular velocity.
        Currently works for rotating links (like crank). 
        For sliders and full 4-bar kinematics, further equations can be added.
        """
        for link in self.links:
            if not link.fixed and link.type == "normal":
                link.angle_deg += np.degrees(link.angular_velocity * dt)

    def get_link_positions(self):
        """
        Returns a list of tuples with start and end positions for each link.
        Simple method: assumes links start from origin or previous joint.
        """
        positions = []
        origin = (0, 0)
        for link in self.links:
            if link.fixed:
                start = origin
                end = (origin[0] + link.length, origin[1])
            elif link.type == "slider":
                start = origin
                end = (origin[0] + link.length, origin[1])
            else:
                angle_rad = np.radians(link.angle_deg)
                start = origin
                end = (start[0] + link.length * np.cos(angle_rad),
                       start[1] + link.length * np.sin(angle_rad))
            positions.append((start, end))
        return positions
