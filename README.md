# ENPM 661 Project 2: BFS Path Planner for a Point Robot
## About
This Project involves a Point Robot in an Enivonment with obstacles, and it must navigate from a start point to a goal point and find the optimal path using the BFS (Breadth First Search) Algorithm. The obstacles in the environment are formed using Semi Algebraic Inequalities and Half Planes

Link to repository : github.com/khuzema-h/Path_Planner

## Dependencies
Ensure you have the following Dependencies in order to run the code
- Python 3
- Matplotlib
- Opencv (cv2)
- Numpy
  
### View Map of Environment
Run **map.py** to view the map generated for the environment

## Running the Code 
- Run the file names **BFS_khuzema_habib.py**
- The program will prompt the user to enter the Start and Goal Coordinates.
- The program will ask the user to re-enter the coordinates if the entered coordinates are on an obstacle or out of bounds
- The program then prints the time taken to find the path in the terminal console and displays an image of the path taken as well as the searched area
- A video file of the animation is saved as 'bfs_path_planner.mp4'

## Sample Code Output

Workspace is 180 mm wide and 50 mm in height, please enter valid coordinates within the given range...

Enter the Start Coordinate(x): 0
Enter the Start Coordinate(y): 0
Start Coordinates are Valid, Proceeding....
Enter Goal coordinate(x): 170
Enter Goal coordinate(y): 20
Goal coordinates are valid. Finding Path with BFS...
Time taken to find the path: 3.1321 seconds
Path found!
Video saved as bfs_path_planner.mp4

