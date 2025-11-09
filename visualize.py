import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class LinkageVisualizer:
    """Visualizes a linkage mechanism using matplotlib."""
    def __init__(self, linkage, title="Mechanical Linkage"):
        self.linkage = linkage
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.ax.set_title(title)

        self.lines = []
        for _ in self.linkage.links:
            line, = self.ax.plot([0, 0], [0, 0], lw=3, marker='o')
            self.lines.append(line)

    def update(self, frame):
        dt = 0.05
        self.linkage.update_positions(dt)
        positions = self.linkage.get_link_positions()

        for i, (start, end) in enumerate(positions):
            self.lines[i].set_data([start[0], end[0]], [start[1], end[1]])

        return self.lines

    def animate(self, frames=500, interval=50):
        anim = FuncAnimation(self.fig, self.update, frames=frames, interval=interval, blit=True)
        plt.show()
