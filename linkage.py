import numpy as np

class Link:
    def __init__(self, name, length, angle_deg=0, fixed=False, angular_velocity=0, type="normal"):
        self.name = name
        self.length = length
        self.angle_deg = angle_deg
        self.fixed = fixed
        self.angular_velocity = angular_velocity
        self.type = type

class Joint:
    def __init__(self, name, x=0, y=0, connects=None, fixed=False):
        self.name = name
        self.x = x
        self.y = y
        self.connects = connects if connects else []
        self.fixed = fixed

class Linkage:
    """Four-bar linkage with proper kinematics."""
    def __init__(self, links_data, joints_data):
        self.links = [Link(**link) for link in links_data]
        self.joints = [Joint(**joint) for joint in joints_data]
        
        self.ground = self.links[0]
        self.crank = self.links[1]
        self.coupler = self.links[2]
        self.rocker = self.links[3]

    def update_positions(self, dt):
        """Update crank angle and compute coupler & rocker positions."""
        self.crank.angle_deg += np.degrees(self.crank.angular_velocity * dt)
        theta2 = np.radians(self.crank.angle_deg)

        L1 = self.ground.length
        L2 = self.crank.length
        L3 = self.coupler.length
        L4 = self.rocker.length
        
        xA, yA = 0, 0
        xB, yB = L1, 0

        xC = xA + L2 * np.cos(theta2)
        yC = yA + L2 * np.sin(theta2)

        dx = xC - xB
        dy = yC - yB
        D = np.hypot(dx, dy)

        if D > (L3 + L4):
            theta4 = 0
            xD = xB + L4
            yD = yB
        else:
            cos_angle = (L4**2 + D**2 - L3**2) / (2 * L4 * D)
            cos_angle = np.clip(cos_angle, -1, 1)
            angle_D = np.arccos(cos_angle)
            theta_D_line = np.arctan2(dy, dx)
            theta4 = theta_D_line - angle_D
            xD = xB + L4 * np.cos(theta4)
            yD = yB + L4 * np.sin(theta4)

        xE, yE = xC, yC

        self.positions = [
            ((xA, yA), (xB, yB)), 
            ((xA, yA), (xC, yC)), 
            ((xC, yC), (xD, yD)),  
            ((xB, yB), (xD, yD))  
        ]

    def get_link_positions(self):
        return getattr(self, 'positions', [])
