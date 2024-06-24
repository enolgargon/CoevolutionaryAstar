import numpy as np
from astar import Node

def return_path(current_node, maze):
    moves = {"R": [0, 1],
             "L": [0, -1],
             "D": [1, 0],
             "U": [-1, 0],
             "H": [0, 0]
             }
    path = []
    no_rows, no_columns = np.shape(maze)
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    result = ""
    for i in range(1, len(path)):
        error = True
        for move in moves.keys():
            if path[i][0] == path[i-1][0] + moves[move][0] and path[i][1] == path[i-1][1] + moves[move][1]:
                result += move
                error = False
        if error:
            raise Exception("Cannot reproduce path")
    return result, path


def search(maze, start, end, cost=1, max_iterations=None):
    """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        :param maze:
        :param cost
        :param start:
        :param end:
        :return:
    """
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    yet_to_visit_list = []
    visited_list = []
    yet_to_visit_list.append(start_node)

    outer_iterations = 0
    if max_iterations is None:
        max_iterations = (len(maze) // 2) ** 10

    move = [[-1, 0],  # go up
            [0, -1],  # go left
            [1, 0],  # go down
            [0, 1]]  # go right

    no_rows, no_columns = np.shape(maze)

    # Loop until you find the end

    while len(yet_to_visit_list) > 0:
        outer_iterations += 1

        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            print("giving up on pathfinding too many iterations")
            return return_path(current_node, maze)

        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node, maze)

        children = []

        for new_position in move:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (no_rows - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost
            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))

            child.f = child.g + child.h
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue
            yet_to_visit_list.append(child)