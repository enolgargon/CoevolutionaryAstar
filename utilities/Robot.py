from utilities import have_collision


class Robot():
    '''
    Class that represents a robot in the problem. It has a copy of the map where move, a starting and ending point, and may have a calculated route.
    '''

    def __init__(self, start_point, end_point, map, route=None):
        '''
        Initializer for the robot.

        :param start_point: Point where the robot starts to move.
        :param end_point: Destination point of the robot.
        :param map: Map where the robot has to move
        :param route: (optional) Route that the robot uses.
        '''
        self.start_point = start_point
        self.end_point = end_point
        self.map = map.copy()
        self.route = route
        self.establish_route = False
        self.collision_point = 0
        self.history_route = []
        if route is not None:
            self.history_route += [route]

    def set_route(self, r):
        '''
        Method that modifies the route of this robot. It allows to mantain an history of routes
        :param r: New route for this robot
        :return: None
        '''
        if r is not None:
            self.history_route += [r]
            self.route = r

    def colision_with(self, other):
        '''
        Method that check if this robot has a collision with another one.

        :param other: Other robot to check
        :return: None if there is not a collition. Position of the collision in other case.
        '''
        self.collision_point = have_collision(self.route, other.route)

        try:
            return self.collision_point[1]
        except:
            return None

    def check_route_valid(self, map=None):
        '''
        Method that check ig a route is valid. It counts the number of times that the robot try to go through an obstacles

        :param map: (optional) Map with the obstacles to check. If not set, attribute map is used
        :return: Number of obstacles in the route of the robot.
        '''
        m = map if map is not None else self.map
        counter = 0

        for i in range(len(self.route[1])):
            if m[self.route[1][i][0], self.route[1][i][1]] == 1:
                counter += 1

        return counter

    def place_obstacle(self, coordinates):
        '''
        Method that modifies the copy of the map that this robot has. It introduces a new obstacle in the coordinates provided.

        :param coordinates: Coordinates X and Y where place the obstacle
        :return: None
        '''
        self.map[coordinates[1], coordinates[0]] = 1

    def __str__(self):
        return self.route.__str__()
