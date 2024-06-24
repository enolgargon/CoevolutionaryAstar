from random import randint, random

MAX_ITER = 100
distancia_max_X = 30
distancia_max_Y = 18

# Dicts used in order to compute somethings below
operations = {
    "H": [0, 0],
    "R": [0, 1],
    "L": [0, -1],
    "D": [1, 0],
    "U": [-1, 0]
}
oposite_operation = {
    "R": "L",
    "L": "R",
    "U": "D",
    "D": "U",
    "H": None
}


def get_mutate_bounds(n, coords_collision):
    dist_x = n / (0.75 * MAX_ITER - 0) * (distancia_max_X - 0.10 * distancia_max_X) + 0.10 * distancia_max_X
    dist_y = n / (0.75 * MAX_ITER - 0) * (distancia_max_Y - 0.10 * distancia_max_Y) + 0.10 * distancia_max_Y
    return (coords_collision[0] - dist_y, coords_collision[1] - dist_x), (
    coords_collision[0] + dist_y, coords_collision[1] + dist_x)


def mutate(route, n_iter, collision_point):
    '''
    Function that makes a mutation on a route.
    It uses random values in order to generate the msp point, the operation to introduce and, if needed, the mep point.

    :param route: Route where make the mutation
    :return: Route after the mutation process
    '''
    # Random msp and operation
    # msp = randint(0, len(route[0]) - 2)
    if collision_point is None:
        r = randint(0, len(route[0]) - 2)
        collision_point = (r, route[1][r])
    mutate_bounds = get_mutate_bounds(n_iter, collision_point[1])
    candidates = []
    for i in range(collision_point[0]):
        coord = route[1][i]
        if coord[0] > mutate_bounds[0][0] and coord[0] < mutate_bounds[1][0] and coord[1] > mutate_bounds[0][1] and \
                coord[1] < mutate_bounds[1][1]:
            candidates += [i]
    msp = candidates[randint(0, len(candidates)-1)] if len(candidates) > 0 else 0

    random_op = randint(0, 9)
    ops = ["R", "L", "D", "U"]
    op = 'H' if random_op > 3 else ops[random_op]
    # check operation valid
    while msp != 0 and route[0][msp - 1] == oposite_operation[op]:
        op = list(operations.keys())[randint(0, 4)]
    if op == 'H':  # HALT, no MEP required
        nr = route[0][:msp] + "H" + route[0][msp:]
    else:  # UP, DOWN, RIGHT or LEFT. generate MEP point and join
        # MEP point and route until there
        mep = randint(msp + 1, len(route[0]) - 1)
        nr = route[0][:msp] + op + route[0][msp:mep]
        points = route_points_from_string(nr, route[1][0])
        # Check if join operation is needed
        if points[-1] in route[1] or points[-2] in route[1]:  # No join operation is needed
            if points[-1] in route[1]:
                mep = route[1].index(points[-1])
            if points[-2] in route[1]:
                nr = nr[:-1]
                mep = route[1].index(points[-2])
        else:  # Join operation is needed
            join_op = find_operation(points[-1], route[1][mep])
            if join_op is not None:
                nr += join_op
        # Complete route
        nr += route[0][mep:]
    return (nr, route_points_from_string(nr, route[1][0]))


def route_points_from_string(string, start):
    '''
    Given and string with operations and starting point calculate the points where the route go through

    :param string: String with operations in route
    :param start: Starting point
    :return: Sequence of points where the route given go through
    '''
    sequence = [start]
    for char in string:
        sequence += [(sequence[-1][0] + operations[char][0], sequence[-1][1] + operations[char][1])]
    return sequence


def find_operation(from_point, to_point):
    '''
    Htlp funcion to make mutetion. Given two points returns the opreration needed to reach the destination point from the departure point.

    :param from_point: From where find the operation
    :param to_point: Point to reach with the operation
    :return: Operation that allows reach the destination point from the departure point. None if no operation allow this
    '''
    for key in operations.keys():
        if from_point[0] + operations[key][0] == to_point[0] and from_point[1] + operations[key][1] == to_point[1]:
            return key
    return None


def execute_tournament(list, p):
    '''
    Function that executes a process of selection using tournament selection.
    The probability (p) of selecting a solution is p*(1-p)^i being i the index of element in the list (from 0).

    :param list: List where select an individual using tournament
    :param p: probability of selection
    :return: Selected item of the list
    '''
    while True:
        r = random()
        sum = 0
        for i in range(len(list)):
            sum += p * ((1 - p) ** i)
            if r < sum:
                return list[i]
