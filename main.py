import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

example_file = "examples/four_bar_example.json" 

with open(example_file, "r") as f:
    mechanism_data = json.load(f)

links = mechanism_data["links"]
joints = mechanism_data["joints"]

print(f"Loaded mechanism: {mechanism_data['mechanism_name']}")
print(mechanism_data["description"])

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-150, 150)
ax.set_ylim(-150, 150)
ax.set_title(mechanism_data["mechanism_name"])

lines = []
for link in links:
    line, = ax.plot([0, 0], [0, 0], lw=3)
    lines.append(line)

crank = links[1]  
theta = np.radians(crank["angle_deg"])
angular_velocity = crank.get("angular_velocity", 1.0) 

def update(frame):
    global theta
    theta += angular_velocity * mechanism_data["simulation"]["time_step"]

    ground_length = links[0]["length"]
    crank_length = crank["length"]

    lines[0].set_data([0, ground_length], [0, 0])

    x_end = crank_length * np.cos(theta)
    y_end = crank_length * np.sin(theta)
    lines[1].set_data([0, x_end], [0, y_end])
    return lines

anim = FuncAnimation(fig, update, frames=500, interval=50, blit=True)
plt.show()
