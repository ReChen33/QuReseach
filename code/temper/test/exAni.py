import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates

# Create initial data
x_data = []
y_data = []

# Create a figure and axis
fig, ax = plt.subplots()
line, = ax.plot_date(x_data, y_data, '-')

# Set axis labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_title('Real-Time Sine Wave with Current Time')

# Set the time format on the x-axis to HH:MM:SS
time_format = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(time_format)

# Function to update the plot
def update(frame):
    current_time = datetime.now()
    new_value = np.sin(frame / 10)  # Generating a sine wave
    x_data.append(current_time)
    y_data.append(new_value)
    line.set_data(x_data, y_data)
    
    # Keep only the last 100 points in the plot
    if len(x_data) > 100:
        x_data.pop(0)
        y_data.pop(0)

    # Set x-axis limits to show the last 5 points and extend 2 seconds beyond the current time
    if len(x_data) > 5:
        time_extension = x_data[-1] + timedelta(seconds=2)
        ax.set_xlim(x_data[-5], time_extension)

    # Adjust y-axis to center the current value
    current_y_range = 1.5 * max(abs(min(y_data)), abs(max(y_data)))  # Ensure some margin
    mid_y_value = new_value
    ax.set_ylim(mid_y_value - current_y_range, mid_y_value + current_y_range)
    
    ax.relim()
    ax.autoscale_view()
    fig.autofmt_xdate()  # Format the x-axis to show time
    return line,

# Create an animation
anim = FuncAnimation(fig, update, frames=np.arange(0, 1000, 0.1), interval=100)

# Show the plot
plt.show()
