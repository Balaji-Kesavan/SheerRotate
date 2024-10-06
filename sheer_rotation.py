import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

def shear_rotation(points, theta):
    """
    Approximates rotation using shear matrices.

    Parameters:
    - points: Nx2 array of (x, y) coordinates.
    - theta: Rotation angle in radians.

    Returns:
    - Transformed points after applying shear-based rotation.
    """
    # Shear factors
    shx = np.tan(theta / 2)
    shy = np.sin(theta)

    # Shear matrices
    Sx = np.array([[1, shx],
                   [0, 1]])
    Sy = np.array([[1, 0],
                   [shy, 1]])

    # Apply shear transformations
    transformed_points = points @ Sx.T @ Sy.T @ Sx.T

    return transformed_points

def exact_rotation(points, theta):
    """
    Rotates points using the exact rotation matrix.

    Parameters:
    - points: Nx2 array of (x, y) coordinates.
    - theta: Rotation angle in radians.

    Returns:
    - Rotated points after applying the exact rotation.
    """
    R = np.array([[np.cos(theta), np.sin(theta)],
                  [-np.sin(theta), np.cos(theta)]])
    return points @ R.T

# Define the vertices of the square with names
square_vertices = {
    'A': np.array([1, 1]),
    'B': np.array([-1, 1]),
    'C': np.array([-1, -1]),
    'D': np.array([1, -1])
}

# Create an array of points for plotting and transformations
square = np.array([square_vertices['A'],
                   square_vertices['B'],
                   square_vertices['C'],
                   square_vertices['D'],
                   square_vertices['A']])  # Close the square

# Set up the plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.grid(True)

# Plot the original square
original_line, = ax.plot(square[:, 0], square[:, 1], 'k-', label='Original Square')
for idx, point_name in enumerate(['A', 'B', 'C', 'D']):
    x, y = square[idx]
    ax.text(x + 0.05, y + 0.05, point_name, color='black')

# Initialize lines for shear-based rotation and exact rotation
shear_line, = ax.plot([], [], 'r--', label='Shear-based Rotation')
exact_line, = ax.plot([], [], 'b-.', label='Exact Rotation')

# Initialize texts for vertex labels
shear_texts = []
exact_texts = []

# Add legend
ax.legend()

# Function to initialize the animation
def init():
    shear_line.set_data([], [])
    exact_line.set_data([], [])
    return shear_line, exact_line

# Function to update the animation at each frame
def animate(frame):
    # Calculate the rotation angle in radians
    angle_deg = frame % 360  # Keep angle between 0-359 degrees
    theta = np.radians(-angle_deg)  # Negative for clockwise rotation

    # Apply shear-based rotation
    shear_rotated_square = shear_rotation(square, theta)

    # Apply exact rotation
    exact_rotated_square = exact_rotation(square, theta)

    # Update shear-based rotation line
    shear_line.set_data(shear_rotated_square[:, 0], shear_rotated_square[:, 1])

    # Update exact rotation line
    exact_line.set_data(exact_rotated_square[:, 0], exact_rotated_square[:, 1])

    # Remove previous texts
    [txt.remove() for txt in shear_texts + exact_texts]
    shear_texts.clear()
    exact_texts.clear()

    # Label vertices for shear-based rotated square
    for idx, point_name in enumerate(["A'", "B'", "C'", "D'"]):
        x, y = shear_rotated_square[idx]
        txt = ax.text(x + 0.05, y + 0.05, point_name, color='red')
        shear_texts.append(txt)

    # Label vertices for exactly rotated square
    for idx, point_name in enumerate(['A"', 'B"', 'C"', 'D"']):
        x, y = exact_rotated_square[idx]
        txt = ax.text(x + 0.05, y + 0.05, point_name, color='blue')
        exact_texts.append(txt)

    # Update the title with the current angle
    ax.set_title(f'Rotation Angle: {angle_deg}°')

    return shear_line, exact_line, *shear_texts, *exact_texts

# Create animation
anim = FuncAnimation(fig, animate, init_func=init,
                     frames=np.arange(0, 360, 30),  # Rotate in 30-degree increments
                     interval=2000, blit=True, repeat=True)

# Display the animation in the notebook
HTML(anim.to_jshtml())