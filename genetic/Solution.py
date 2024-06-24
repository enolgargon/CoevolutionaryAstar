from utilities import have_obstacle, have_collision


class Solution:
    '''
    Class that represent a posible solution in the Genetic Algorithm.
    It contains a route that may be a possible solution to the problem and a fitness value that represents the quality of the solution.
    '''

    def __init__(self, route, map=None):
        '''
        Initializer for the solucion

        :param route: Route that provide a possible solution.
        :param map: (optional) Map to check collisions
        '''
        self.route = route
        self.collision_point = None
        if map is not None:
            self.calculate_fitness(map)

    def calculate_fitness(self, map, other_solutions=None):
        '''
        Method that updates the fitness values for this solution
        Fitness values are 3 different attributes that contains lenght, number of collision and if has an obstacle or not.

        :param map: Map to check obstacles
        :param other_solutions: List with other routes to check collisions
        :return: None
        '''
        self.colisions, self.length, self.obstacles = fitness(self, map, other_solutions)

    def get_sort_value(self, max_length):
        '''
        This method generates a custom value for sorting in order to make a sort taking into account the collisions of the solutions and length of it.

        :param max_length: Max lenght of the solutions to order in order to make a priority of obstacles
        :return: Value to order the solution list (1000000 if contains an obstacle)
        '''
        if self.obstacles:
            return 1000000
        else:
            return self.colisions * max_length + self.length

    def __str__(self):
        return f"{self.route[0]}\t{self.colisions}\t{self.length}\t{self.obstacles}"


def fitness(solution, map, other_routes=None):
    '''
    Function that computes the fitness values of a possible solution.

    :param solution: Solution to evaluate using the fitness function
    :param map: Map where the route are calculated in order to check collision with obstacles
    :param other_routes: (optional) Other routes to check collision with
    :return: Tuple. Number of collisions with other routes, length of the solution and a boolean that represents if there are obstacles in the route.
    '''
    # If there is other routes to compare, penalise one point for each route with cllisions.
    collisions = 0
    if other_routes is not None:
        for route in other_routes:
            if isinstance(route, list) and len(route) == 1:
                route = route[0]
            solution.collision_point = have_collision(solution.route, route.route if isinstance(route, Solution) else route)
            if solution.collision_point is None:
                collisions += 1
    return collisions, len(solution.route[0]), have_obstacle(map, solution.route)
