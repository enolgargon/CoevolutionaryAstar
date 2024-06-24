from random import randint

from utilities import load_obstacle_matrix

if __name__ == '__main__':
    n_robots = 200
    n_habs = 1

    matrix = load_obstacle_matrix('scenario3/scenery_warehouse.txt')
    points = []

    for i in range(n_robots * 2 * n_habs):
        while True:
            y = randint(0, len(matrix) - 1)
            x = randint(0, len(matrix[0]) - 1)
            if matrix[y][x] == 0:
                matrix[y][x] = 1
                break
        points += [[x, y]]

    for dx in [0]:#, 32]:
        for dy in [0]:#, 12]:
            for i in range(n_robots):
                p1 = points.pop(randint(0, len(points) - 1))
                p2 = points.pop(randint(0, len(points) - 1))
                print(f'{p1[0] + dx},{p1[1] + dy};{p2[0] + dx},{p2[1] + dy}')
