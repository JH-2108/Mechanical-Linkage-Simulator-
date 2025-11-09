import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from linkage import Linkage
from visualize import LinkageVisualizer

example_file = "examples/four_bar_example.json"
with open(example_file, "r") as f:
    mech_data = json.load(f)

linkage = Linkage(mech_data["links"], mech_data["joints"])

visualizer = LinkageVisualizer(linkage, mech_data["mechanism_name"])
visualizer.animate()

example_file = "examples/four_bar_example.json" 
with open(example_file, "r") as f:
    mech_data = json.load(f)

links = mech_data["links"]
joints = mech_data["joints"]

print(f"Loaded mechanism: {mech_data['mechanism_name']}")
print(mech_data["description"])

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-200, 200)
ax.set_ylim(-200, 200)
ax.set_title(mech_data["mechanism_name"])

lines = []
for link in links:
    line, = ax.plot([0, 0], [0, 0], lw=3, marker='o')
    lines.append(line)

crank = links[1]  
theta = np.radians(crank.get("angle_deg", 0))
angular_velocity = crank.get("angular_velocity", 1.0) 

def get_joint_pos(link_name, link_angle_deg, link_length, origin=(0, 0)):
    """Calculate the (x, y) of the end of a link given its angle and length."""
    x = origin[0] + link_length * np.cos(np.radians(link_angle_deg))
    y = origin[1] + link_length * np.sin(np.radians(link_angle_deg))
    return x, y

def update(frame):
    global theta
    theta += angular_velocity * mech_data["simulation"]["time_step"]
    
    ground = links[0]
    lines[0].set_data([0, ground["length"]], [0, 0])
    
    crank_length = crank["length"]
    crank_x, crank_y = get_joint_pos(crank["name"], np.degrees(theta), crank_length)
    lines[1].set_data([0, crank_x], [0, crank_y])

    if mech_data["mechanism_name"].lower().find("four-bar") != -1:
        coupler = links[2]
        rocker = links[3]

        coupler_x, coupler_y = crank_x + coupler["length"], crank_y
        lines[2].set_data([crank_x, coupler_x], [crank_y, coupler_y])
        
        rocker_x, rocker_y = coupler_x + rocker["length"], 0
        lines[3].set_data([coupler_x, rocker_x], [coupler_y, rocker_y])

    elif mech_data["mechanism_name"].lower().find("crank-slider") != -1:
        connecting_rod = links[2]
        slider = links[3]

        crank_end_x, crank_end_y = crank_x, crank_y

        rod_x, rod_y = crank_end_x + connecting_rod["length"], crank_end_y
        lines[2].set_data([crank_end_x, rod_x], [crank_end_y, rod_y])
        
        slider_x = rod_x
        slider_y = 0
        lines[3].set_data([rod_x, slider_x], [rod_y, slider_y])

    return lines

anim = FuncAnimation(fig, update, frames=500, interval=50, blit=True)
plt.show()
