from Map import *
import numpy as np
import math

# Node object to keep track of the different nodes properties.
class Node:
    def __init__(self, coordinates, previousNode):
        self.coordinates = coordinates
        self.previousNode = previousNode

        self.g = 0  # Initialize g-score
        self.h = 0  # Initialize h-score
        self.f = 0  # Initialize f-score
        self.value = 0

    # Calculates and sets the f-score
    def CalculateF(self):
        self.f = self.g + self.h

    # Stores the value/label of the position
    def GetValue(self):
        self.value = data[self.coordinates[0]][self.coordinates[1]]


# Calculates the H-score (which is the Euclidean Distance)
# We want this low because the closer we are the better.
def Euclidean_distance(currentPos, endPos):
    dx = endPos[0] - currentPos[0]
    dy = endPos[1] - currentPos[1]
    return math.sqrt(dx * dx + dy * dy)


# Function that returns the node in array with lowest f-cost
def findBestNode(array):
    bestNode = array[0]
    for node in array:
        if node.f < bestNode.f:
            bestNode = node
    return bestNode


def Algorithm_star(data, start, end):
    path = []  # Path to goal, array with nodes
    not_visited = []  # Nodes not visited but under consideration
    visited = []  # Nodes done with

    start = Node(start, None)  # Start node
    end = Node(end, None)  # End node

    start.h = Euclidean_distance(start.coordinates, end.coordinates)  # Sets the start node h-score
    start.CalculateF()  # F-score

    currentNode = start  # Start by the first node

    # Adds the start point to not visited and visited list to use as the first point we move from.
    not_visited.append(start)
    visited.append(start)
    going = True

    # Increase the i-max value if you increase the map size
    i = 0

    while going:
        i += 1
        if i == 1000:
            for node in not_visited:
                data[node.coordinates[0]][node.coordinates[1]] = 5
            going = False

        # Calculate neighbor nodes and its costs
        neighbor_list = []

        # CASE FOR LEFT NODE COORDINATE
        if currentNode.coordinates[1] - 1 < 39:  # The y-axis is 39 pixels long
            left = Node((currentNode.coordinates[0], currentNode.coordinates[1] - 1), currentNode)
            left.h = Euclidean_distance(left.coordinates, end.coordinates)  # h-score
            left.GetValue()  # value
            left.g = currentNode.g + left.value  # g-score
            left.CalculateF()  # f-value

            # If the value is not a wall we added to the list
            if left.value != -1:
                neighbor_list.append(left)

        # CASE FOR RIGHT NODE COORDINATE
        if currentNode.coordinates[1] + 1 < 39:  # The y-axis is 39 pixels long
            right = Node((currentNode.coordinates[0], currentNode.coordinates[1] + 1), currentNode)
            right.h = Euclidean_distance(right.coordinates, end.coordinates)  # h-score
            right.GetValue()  # value
            right.g = currentNode.g + right.value  # g-score
            right.CalculateF()  # f-value

            # If the value is not a wall we added to the list
            if right.value != -1:
                neighbor_list.append(right)

        # CASE FOR ABOVE NODE COORDINATE
        if currentNode.coordinates[0] - 1 < 47:  # The x-axis is 47 pixels long
            up = Node((currentNode.coordinates[0] - 1, currentNode.coordinates[1]), currentNode)
            up.h = Euclidean_distance(up.coordinates, end.coordinates)  # h-score
            up.GetValue()  # value
            up.g = currentNode.g + up.value  # g-score
            up.CalculateF()  # f-value

            # If the value is not a wall we added to the list
            if up.value != -1:
                neighbor_list.append(up)

        # CASE FOR BELOW NODE COORDINATE
        if currentNode.coordinates[0] + 1 < 47:  # The x-axis is 47 pixels long
            down = Node((currentNode.coordinates[0] + 1, currentNode.coordinates[1]), currentNode)
            down.h = Euclidean_distance(down.coordinates, end.coordinates)  # h-score
            down.GetValue()  # value
            down.g = currentNode.g + down.value  # g-score
            down.CalculateF()  # f-value

            # If the value is not a wall we added to the list
            if down.value != -1:
                neighbor_list.append(down)

        # Update the list
        for node in neighbor_list:
            check = False

            # If they are in the not_visited list, remove them
            for not_visited_node in not_visited:
                if node.coordinates == not_visited_node.coordinates:
                    check = True

            # If they are in the visited list, remove them
            for visited_node in visited:
                if node.coordinates == visited_node.coordinates:
                    check = True

            # adds to not_visited list if is not a wall, not already in consideration or visited
            if check == False:
                not_visited.append(node)

        prevNode = currentNode  # Previous node
        currentNode = findBestNode(not_visited)  # Smallest f-score and set it as current node


        if currentNode != prevNode:
            not_visited.remove(currentNode)  # Remove currentNode since we have chosen prevNode
            visited.append(currentNode)  # Add it to visited

        # We found the next biggest
        elif currentNode == prevNode:
            currentNode = findBestNode(not_visited)
            not_visited.remove(currentNode)  # Remove currentNode since we have chosen another Node
            visited.append(currentNode)  # Add it to visited

        # We got to our end node, the goal
        if currentNode.coordinates[0] == end.coordinates[0] and currentNode.coordinates[1] == end.coordinates[1]:

            # Retrieve the path taken to the goal
            path.append(currentNode)  # Where current node is actually the end node
            previousNode = currentNode.previousNode
            j = 0
            while previousNode != None:
                j += 1
                if j == 100:
                    break
                path.append(previousNode) # Store them in the path list
                previousNode = previousNode.previousNode

            # Update the value of the node and put a '5' so it states that is the way the path goes
            for node in path:
                data[node.coordinates[0], node.coordinates[1]] = 5

            # Return as an array
            return np.array(data)

# To show the map with the path. Copied from Map.py
def drawPath(map):
    # Define width and height of image
    width = map.shape[1]
    height = map.shape[0]
    # Define scale of the image
    scale = 20
    # Create an all-yellow image
    image = Image.new('RGB', (width * scale, height * scale), (255, 255, 0))
    # Load image
    pixels = image.load()
    # Define what colors to give to different values of the string map
    # (undefined values will remain yellow, this is
    # how the yellow path is painted)
    colors = {
        -1: (211, 33, 45),
        1: (215, 215, 215),
        2: (166, 166, 166),
        3: (96, 96, 96),
        4: (36, 36, 36),
        5: (255, 251, 0)  # Yellow
    } # Now we have different labels so we change the keys
    # Go through image and set pixel color for every position
    for y in range(height):
        for x in range(width):
            if map[y][x] not in colors: continue
            for i in range(scale):
                for j in range(scale):
                    pixels[x * scale + i, y * scale + j] = colors[map[y][x]]
    # Show image
    image.show()

# Declare HERE the task:
task = 4

# Initialise map and data object
if task == 1:
    map = Map_Obj(task=1)
    data, size = map.read_map("/Users/martaalmagro/PycharmProjects/pythonProject/Samfundet_map_1.csv")
if task == 2:
    map = Map_Obj(task=2)
    data, size = map.read_map("/Users/martaalmagro/PycharmProjects/pythonProject/Samfundet_map_1.csv")
if task == 3:
    map = Map_Obj(task=3)
    data, size = map.read_map("/Users/martaalmagro/PycharmProjects/pythonProject/Samfundet_map_2.csv")
if task == 4:
    map = Map_Obj(task=4)
    data, size = map.read_map("/Users/martaalmagro/PycharmProjects/pythonProject/Samfundet_map_Edgar_full.csv")

# Get the initial and en positions
start_pos = map.get_start_pos()
end_pos = map.get_end_goal_pos()

# Apply algorithm
data = Algorithm_star(data, start_pos, end_pos)
print(data)

# In order to show the image we are going to copy show_map function and insert it the data of the map
drawPath(data)
