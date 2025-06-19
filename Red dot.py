import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.patches import Circle

# Create figure and axis
fig, ax = plt.subplots(figsize=(4, 4))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# Central red dot without outline
center_dot = Circle((0, 0), 0.12, facecolor='red', edgecolor='none', linewidth=0, alpha=1.0)
ax.add_patch(center_dot)

# Pulse ring without outline, just red fill
pulse_ring = Circle((0, 0), 0.2, facecolor='red', edgecolor='none', linewidth=0, alpha=0.5)
ax.add_patch(pulse_ring)

# Animation function
def animate_no_outline(frame):
    scale = 0.2 + frame / 40.0 * 0.6
    alpha = max(0.5 - frame / 40.0, 0)
    pulse_ring.set_radius(scale)
    pulse_ring.set_alpha(alpha)
    center_dot.set_alpha(0.7 + 0.3 * np.sin(frame * 0.3))
    return pulse_ring, center_dot

# Create animation
ani_no_outline = animation.FuncAnimation(fig, animate_no_outline, frames=40, interval=50, blit=True)

# Save GIF
ani_no_outline.save("red_pulse_no_outline.gif", writer='pillow', fps=20, savefig_kwargs={'transparent': True})
