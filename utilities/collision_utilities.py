def have_collision(route_1, route_2):
    '''
    Function that checks if exist any collision between two routes.
    NOTE: this function checks if there is a collision of route 1 with route 2, but not necessary of route 2 with route 1.

    :param route_1: Route that want to check if has solucion
    :param route_2: Other route to compare with
    :return: Point where collission happen or None if there is not collision
    '''
    if route_1 is None or route_2 is None: # check valid params
        raise Exception("No calculated route to check collisions")

    for i in range(len(route_1[1])):
        # Check if the routes have a collision on a cell
        if route_1[1][i] == route_2[1][i if i < len(route_2[1]) else -1]: # the inline if check if route 2 has finished. In this case takes as point the destination point of route 2.
            return i, route_1[1][i]
        # Check if the routes cross between two cells
        if i > 0 and len(route_2[1]) > i and route_1[1][i] == route_2[1][i - 1] and route_1[1][i - 1] == route_2[1][i]:
            return i, route_1[1][i]
    return None


def have_obstacle(map, route):
    '''
    Given the map and a route, this function checks if the route have a collision with any obstacle in there.

    :param map: Map with obstacles.
    :param route: Route to check
    :return: Boolean. True if there is any collision, false in other case.
    '''
    for i in range(len(route[1])):
        if map[route[1][i][0]][route[1][i][1]] == 1:
            return True
    return False
