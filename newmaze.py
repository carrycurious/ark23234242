import cv2
import numpy as np
import random
import math
import matplotlib.pyplot as plt

# Load and process the maze
maze = cv2.imread(r'C:\Users\sandeep\Downloads\maze.png', cv2.IMREAD_GRAYSCALE)
_, maze = cv2.threshold(maze, 127, 255, cv2.THRESH_BINARY)


start1 = (39, 316)  


endy1 = 316  
endxrange = (76, 122)  


def isline(point):
    
    x, y = point
    return y == endy1 and endxrange[0] <= x <= endxrange[1]


# Parameters
step_size = 10  
max_iterations = 100000


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def isfree(p1, p2, maze):
    
    num_points = max(int(distance(p1, p2) / 2), 1)  #
    for i in range(num_points + 1):
        x = int(p1[0] + (p2[0] - p1[0]) * i / num_points)
        y = int(p1[1] + (p2[1] - p1[1]) * i / num_points)
        if maze[y, x] == 0:  # Black pixel means obstacle
            return False
    return True





class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent





def move_towards(q_near, q_rand, step_size):
    """Move from q_near towards q_rand by step_size."""
    theta = math.atan2(q_rand[1] - q_near.y, q_rand[0] - q_near.x)
    x_new = int(q_near.x + step_size * math.cos(theta))
    ynew = int(q_near.y + step_size * math.sin(theta))
    return x_new, ynew


# Initialize RRT
rrt = [Node(start1[0], start1[1])]
found = False

for _ in range(max_iterations):
    qrand = random.randint(0, maze.shape[1] - 1), random.randint(0, 330)
    qnear = min(rrt, key=lambda node: distance((node.x, node.y), qrand))
    qnew = move_towards(qnear, qrand, step_size)
    
    if isfree((qnear.x, qnear.y), qnew, maze):
        new_node = Node(qnew[0], qnew[1], qnear)
        rrt.append(new_node)
        
        if isline(qnew):  # Stop when reaching the end line
            found = True
            end_node = Node(qnew[0], qnew[1], new_node)
            rrt.append(end_node)
            break

# Extract and visualize path
if found:
    path = []
    node = rrt[-1]
    while node:
        path.append((node.x, node.y))
        node = node.parent
    path.reverse()
    
    # Draw path on the maze
    for i in range(len(path) - 1):
        cv2.line(maze, path[i], path[i + 1], (127), 2)

    plt.imshow(maze, cmap='gray')
    plt.show()
else:
    print("No path found!")  