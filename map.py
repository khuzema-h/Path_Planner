import numpy as np
import matplotlib.pyplot as plt

# Define the map dimensions (50 rows x 180 columns)
map_height = 50
map_width = 180

# Create a grid for visualization
x = np.linspace(0, map_width, 500)
y = np.linspace(0, map_height, 500)
X, Y = np.meshgrid(x, y)

# Define the shapes using semi-algebraic models
def shape_E(x, y):
    # Bottom corner starts at (10, 10)
    # Letter height: 25, Letter width: 13
    # Vertical line
    vertical = (10 <= x) & (x <= 15) & (10 <= y) & (y <= 35)
    # Top horizontal line
    top_horizontal = (10 <= x) & (x <= 23) & (30 <= y) & (y <= 35)
    # Middle horizontal line
    middle_horizontal = (10 <= x) & (x <= 23) & (20 <= y) & (y <= 25)
    # Bottom horizontal line
    bottom_horizontal = (10 <= x) & (x <= 23) & (10 <= y) & (y <= 15)
    return vertical | top_horizontal | middle_horizontal | bottom_horizontal

def shape_N(x, y):
    # Bottom corner starts at (28, 10) (adjusted to add 5 units of space after E)
    # Letter height: 25, Letter width: 15
    # Left vertical line
    left_vertical = (28 <= x) & (x <= 33) & (10 <= y) & (y <= 35)
    # Diagonal line: starts at top of left vertical (x=28, y=35) and ends at bottom of right vertical (x=43, y=10)
    # Constrain the diagonal to stay within y = 10 to y = 35
    diagonal = (y >= -2.5 * (x - 28) + 35) & (y <= -2.5 * (x - 33) + 35) & (28 <= x) & (x <= 43) & (10 <= y) & (y <= 35)
    # Right vertical line
    right_vertical = (38 <= x) & (x <= 43) & (10 <= y) & (y <= 35)
    return left_vertical | diagonal | right_vertical

def shape_P(x, y):
    # Vertical line
    vertical = (48 <= x) & (x <= 53) & (10 <= y) & (y <= 35)
    # Semi-circle with radius 6, centered at the top of the vertical line (x=53, y=35)
    semi_circle = ((x - 53)**2 + (y - 29)**2 <= 6**2) & (x >= 53)
    return vertical | semi_circle

def shape_M(x, y):
    # Bottom corner starts at (64, 10)
    # Letter height: 25, Letter width: 28
    # Left vertical line
    left_vertical = (64 <= x) & (x <= 69) & (10 <= y) & (y <= 35)
    # Diagonal line: starts at top of left vertical (x=64, y=35) and ends at bottom of right vertical (x=79, y=10)
    diagonal = (y >= -2.5 * (x - 64) + 35) & (y <= -2.5 * (x - 69) + 35) & (64 <= x) & (x <= 79) & (10 <= y) & (y <= 35)
    # Bottom horizontal line
    bottom_horizontal = (75 <= x) & (x <= 82) & (10 <= y) & (y <= 15)
    # Diagonal 2: starts at top of right vertical (x=87, y=35) and ends at bottom of bottom horizontal (x=79, y=10)
    diagonal_2 = (y >= 2.5 * (x - 92) + 35) & (y <= 2.5 * (x - 87) + 35) & (79 <= x) & (x <= 87) & (10 <= y) & (y <= 35)
    # Right vertical line
    right_vertical = (87 <= x) & (x <= 92) & (10 <= y) & (y <= 35)
    return left_vertical | diagonal | bottom_horizontal | diagonal_2 | right_vertical

def shape_6(x, y):
    # Bottom corner starts at (97, 10) (5 units after the M, which ends at x=92)
    # Character height: 25, Character width: 18
    # Center of the circles
    center_x, center_y = 106, 19
    # Outer circle (radius = 9)
    outer_circle = ((x - center_x)**2 + (y - center_y)**2 <= 9**2) & (97 <= x) & (x <= 115) & (10 <= y) & (y <= 38)
    # Inner circle (radius = 6, to create the "6" shape)
    inner_circle = ((x - center_x)**2 + (y - center_y)**2 <= 4**2) & (97 <= x) & (x <= 115) & (10 <= y) & (y <= 38)
    vertical_line = (97 <= x) & (x <= 102) & (19 <= y) & (y <= 38)
    return outer_circle & ~inner_circle | vertical_line 

def shape_1(x,y):
    vertical_line = (143 <= x) & (x <= 148) & (10 <= y) & (y <= 38)
    return vertical_line


# Combine all shapes
def all_shapes(x, y):
    return shape_E(x, y) | shape_N(x, y) | shape_P(x,y) | shape_M(x,y) | shape_6(x,y) | shape_6(x-23,y) | shape_1(x,y)

# Evaluate the shapes on the grid
Z = all_shapes(X, Y)

# Plot the shapes
plt.figure(figsize=(18, 5))
plt.imshow(Z, extent=(0, map_width, 0, map_height), origin='lower', cmap='binary', alpha=0.8)
plt.title("Map with Obstacles")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.grid(True, which='both', color='gray', linestyle='--', linewidth=0.5)
plt.show()

