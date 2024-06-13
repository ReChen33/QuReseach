import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the figure and subplots (four x-y planes)
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Flatten the axes array for easier iteration
ax1, ax2, ax3, ax4 = axs.flatten()

# Set up the axis limits for all subplots
for ax in (ax1, ax2, ax3, ax4):
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-2, 2)

# Create four line objects, one for each subplot

line1, = ax1.plot([], [], lw=2, label='sin(x)')
line2, = ax2.plot([], [], lw=2, label='sin(2x)')
line3, = ax3.plot([], [], lw=2, label='sin(3x)')
line4, = ax4.plot([], [], lw=2, label='sin(4x)')

# Add legends to each subplot
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()

# Initialize the lines
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    return line1, line2, line3, line4

# Update the lines for each frame
def update(frame):
    x = np.linspace(0, 2 * np.pi, 1000)
    y1 = np.sin(x + frame / 10.0)
    y2 = np.sin(2 * x + frame / 10.0)
    y3 = np.sin(3 * x + frame / 10.0)
    y4 = np.sin(4 * x + frame / 10.0)
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    line3.set_data(x, y3)
    line4.set_data(x, y4)

    ax1.text(1, 0, y1, transform=ax1.transAxes, 
            color='#777777', size=46, ha='right',
            weight=800,bbox=dict(facecolor='white', alpha=1))  
      
    return line1, line2, line3, line4

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 200), init_func=init, blit=True)

# Display the animation
plt.show()
