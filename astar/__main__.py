from astar import search
import numpy as np

if __name__ == '__main__':
    base_path = "F:\\MultirobotRouting\\"
    with open(f'{base_path}scenery.txt') as f:
        lines = f.read().splitlines()
    matrix = np.zeros(shape=(len(lines), max([len(lines[i]) for i in range(len(lines))])))
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '#':
                matrix[i,j] = 1
    print(matrix)
    start = [8, 7]  # starting position
    end = [5, 25]  # ending position

    path = search(matrix, start, end)
    print(path)