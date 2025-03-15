import numpy as np
import matplotlib.pyplot as plt
import time
import cv2
from collections import deque

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
    return outer_circle & & np.logical_not(inner_circle) | vertical_line 

def shape_1(x,y):
    vertical_line = (143 <= x) & (x <= 148) & (10 <= y) & (y <= 38)
    return vertical_line

# Combine all shapes
def all_shapes(x, y):
    return shape_E(x, y) | shape_N(x, y) | shape_P(x, y) | shape_M(x, y) | shape_6(x, y) | shape_6(x - 23, y) | shape_1(x, y)

# Create a blank white image
width, height = 180, 50  # Dimensions in millimeters
mm_to_pixels = 5  # Conversion factor from mm to pixels
width_pixels = int(width * mm_to_pixels)
height_pixels = int(height * mm_to_pixels)
image = np.ones((height_pixels, width_pixels, 3), dtype=np.uint8) * 255  # White background

# Iterate over each pixel in the image
for x in range(width_pixels):
    for y_opencv in range(height_pixels):
        y = height_pixels - 1 - y_opencv  # Flip y-coordinate when reading with opencv to ensure that the origin is at the bottom left
        if all_shapes(x / mm_to_pixels, y / mm_to_pixels):
            image[y_opencv, x] = 0  # Mark the pixel as part of the obstacle

# Add 2 mm clearance around obstacles
clearance_pixels = int(2 * mm_to_pixels)  # Convert 2 mm to pixels
kernel = np.ones((clearance_pixels, clearance_pixels), np.uint8)  # Create a kernel for dilation
dilated_image = cv2.dilate(image[:, :, 0], kernel, iterations=1)  # Dilate the obstacle regions
image[dilated_image == 0] = 0  # Update the image with the expanded obstacles

# Define the actions as separate functions
def move_right(node):
    return (node[0] + 1, node[1])

def move_left(node):
    return (node[0] - 1, node[1])

def move_up(node):
    return (node[0], node[1] + 1)

def move_down(node):
    return (node[0], node[1] - 1)

def move_up_right(node):
    return (node[0] + 1, node[1] + 1)

def move_up_left(node):
    return (node[0] - 1, node[1] + 1)

def move_down_right(node):
    return (node[0] + 1, node[1] - 1)

def move_down_left(node):
    return (node[0] - 1, node[1] - 1)

# Define the actions set
actions_set = [move_right, move_left, move_up, move_down, move_up_right, move_up_left, move_down_right, move_down_left]

# BFS algorithm
def bfs(start, goal, map):
    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    came_from = {}
    path_iteration = 0

    while queue:
        current_node = queue.popleft()

        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()

            for node in path:
                map[node[1], node[0]] = [0, 0, 255]  # Mark the path in red

            frame = cv2.cvtColor(map, cv2.COLOR_RGB2BGR)
            out.write(frame)

            return path

        for action in actions_set:
            next_node = action(current_node)

            if (0 <= next_node[0] < map.shape[1]) and (0 <= next_node[1] < map.shape[0]) and (next_node not in visited) and (np.array_equal(map[next_node[1], next_node[0]], [255, 255, 255])):
                queue.append(next_node)
                visited.add(next_node)
                came_from[next_node] = current_node
                map[next_node[1], next_node[0]] = [255, 100, 0]  # Mark scanned pixels in green

                if path_iteration % 100 == 0:  # Write every 100 iterations
                    frame = cv2.cvtColor(map, cv2.COLOR_RGB2BGR)
                    out.write(frame)
                path_iteration += 1

    return None  # No path found

# Video setup
video_name = 'bfs_path_planner.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
out = cv2.VideoWriter(video_name, fourcc, 120, (width_pixels, height_pixels))  # 120 fps for a quicker animation

# Start Screen
print(r"""____________ _____  ______     _   _      ______ _                             
| ___ \  ___/  ___| | ___ \   | | | |     | ___ \ |                            
| |_/ / |_  \ `--.  | |_/ /_ _| |_| |__   | |_/ / | __ _ _ __  _ __   ___ _ __ 
| ___ \  _|  `--. \ |  __/ _` | __| '_ \  |  __/| |/ _` | '_ \| '_ \ / _ \ '__|
| |_/ / |   /\__/ / | | | (_| | |_| | | | | |   | | (_| | | | | | | |  __/ |   
\____/\_|   \____/  \_|  \__,_|\__|_| |_| \_|   |_|\__,_|_| |_|_| |_|\___|_|   
                                                                               
                                                                               """)

# Get start and goal coordinates from the user
print("Workspace is 180 mm wide and 50 mm in height, please enter valid coordinates within the given range... \n")
while True:
    start_x = int(input("Enter the Start Coordinate(x): "))
    start_y = int(input("Enter the Start Coordinate(y): "))
    start_x += 1
    start_y += 1

    start_x_px = mm_to_pixels * start_x
    start_y_px = height_pixels - (mm_to_pixels * start_y)  # Flip y-coordinate

    if (0 <= start_x_px < width_pixels) and (0 <= start_y_px < height_pixels):
        start_pixel_value = image[start_y_px, start_x_px]
        if np.array_equal(start_pixel_value, [255, 255, 255]):
            print("Start Coordinates are Valid, Proceeding....")
            break
        else:
            print("Coordinates are on an obstacle, please re-enter valid coordinates...")
    else:
        print("Coordinates are out of bounds, please re-enter valid coordinates...")

while True:
    goal_x = int(input("Enter Goal coordinate(x): "))
    goal_y = int(input("Enter Goal coordinate(y): "))

    goal_x_px = mm_to_pixels * goal_x
    goal_y_px = height_pixels - (mm_to_pixels * goal_y)  # Flip y-coordinate

    if (0 <= goal_x_px < width_pixels) and (0 <= goal_y_px < height_pixels):
        goal_pixel_value = image[goal_y_px, goal_x_px]
        if np.array_equal(goal_pixel_value, [255, 255, 255]):
            print("Goal coordinates are valid. Finding Path with BFS...")
            break
        else:
            print("Coordinates are on an obstacle, please re-enter valid coordinates...")
    else:
        print("Coordinates are out of bounds, please re-enter valid coordinates...")

# Run BFS algorithm
start_time = time.time()
start_node = (start_x_px, start_y_px)
goal_node = (goal_x_px, goal_y_px)
path = bfs(start_node, goal_node, image)
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to find the path: {time_taken:.4f} seconds")

# Display the final path
if path:
    print("Path found!")
else:
    print("No path found.")

# Display the final image
cv2.imshow('BFS Path Planner', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
cv2.destroyAllWindows()

# Release the video writer
out.release()
print(f"Video saved as {video_name}")
