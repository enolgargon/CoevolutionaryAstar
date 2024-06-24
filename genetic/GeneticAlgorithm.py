from random import randint
from utilities import have_collision
import numpy as np
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


from genetic import Solution, mutate, execute_tournament


class GeneticAlgorithm():
    '''
    Class that defines de process of the genetic algoritm and store all the information needed
    '''

    def __init__(self, robots, map, p_size=9, q=1, p_eval=0.5, k=3, p_sel=0.35):
        '''
        Initialices the Genetic algorithm

        :param robots: Robots thatbe used for calculate routes.
        :param map: Original map where the robots move.
        '''
        self.iteration = 0
        self.robots = robots
        self.map = np.copy(map)
        self.p_size = p_size
        self.q = q
        self.p_eval = p_eval
        self.k = k
        self.p_sel = p_sel
        self.population = []
        self.init_population()

    def init_population(self):
        '''
        Function that initialice the initial population for the genetic algoritm. It takes the history of routes of the robors, get q routes from each one in order to evaluate and evaluate and add all the possible solution to the initial population.

        :return: None
        '''
        # Get Q random routes to evaluate the fitness of the initial population.
        routes = []
        for robot in self.robots:
            r = []
            generated = []  # Random values used in each robot. Avoid use twice the same route.
            for i in range(self.q):
                n = randint(0, len(robot.history_route) - 1)
                while n in generated:  # Continue generating until get new one not generated before
                    n = randint(0, len(robot.history_route) - 1)
                generated += [n]
                r += [robot.history_route[n]]  # Get a route from this robot using random value
            routes += [r]
        # Take all the routes and evaluate their fitness value
        for i in range(len(self.robots)):
            # Create an array with que q routes of other robots to calculate fitness value.
            other = np.copy(routes)
            np.delete(other, i)
            other = np.concatenate(other)
            r = []
            # Get all the routes of this robor
            for route in self.robots[i].history_route:
                # Create a solucion and evaluate it
                s = Solution(route)
                s.calculate_fitness(self.map, other)
                r += [s]
            self.population += [r]

    def mutate_operation(self, i, evaluation_individuals):
        for j in range(len(self.population[i])):  # Solution by solution executes the mutation process
            s = Solution(mutate(self.population[i][j].route, self.iteration, self.population[i][j].collision_point))
            s.calculate_fitness(self.map, evaluation_individuals)
            self.robots[i].collision_point = s.collision_point
            self.new_population[i] += [s]

    def make_iteration(self):
        '''
        Funtion that executes an iteration (generation) of the genetic algorithm
        :return: None
        '''
        # Get individuals from the previous population in order to calculate the fitness value of new solutions
        evaluation_individuals = self.get_q_individuals()
        self.new_population = np.copy(self.population) # Incremental mutation. Candidate solutions are previuos ones and the new ones generated
        for i in range(len(self.new_population)):
            if not isinstance(self.new_population[i], (list, np.ndarray, np.generic)):
                self.new_population[i] = [self.new_population[i]]
            if isinstance(self.new_population[i], (np.ndarray, np.generic)):
                self.new_population[i] = self.new_population[i].tolist()
        if isinstance(self.new_population, (np.ndarray, np.generic)):
            self.new_population = self.new_population.tolist()

        threads = []
        for i in range(len(self.population)): # For each robot
            if self.robots[i].establish_route:
                continue
            t = Thread(target=self.mutate_operation, args=(i, evaluation_individuals))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        # Makes a selection and save results_old of this iteration/generation as the new population
        self.population = self.make_selection(self.new_population)
        self.iteration += 1
        return self.evaluate()

    def selection_operation(self, population):
        r_selected = []  # Array where store the selected solutions for this robot
        r_population = list(population)
        max_length = max(map(lambda x: x.length, r_population))
        r_population.sort(key=lambda x: x.get_sort_value(max_length))
        # Elitism
        if isinstance(r_population, list):
            j = 0
            while len(r_population) > 0 and j < self.k:
                r_selected += [r_population.pop(0)]
                j += 1
        else:
            r_selected = r_population

        # Tournament
        # It make PS - k groups in order to fill population with PS individuals (currently the population have k indiviudals from elitism)
        if isinstance(r_population, list):
            t_size = len(r_population) // (self.p_size - self.k)
            if t_size > 0:
                for j in range(self.p_size - self.k):
                    if j == self.p_size - self.k - 1:  # i takes last value
                        # Not set finish index in order to avoid not using last element because population length may not be multiplot of PS-k
                        r_selected += [execute_tournament(r_population[j * t_size:], self.p_sel)]
                    else:
                        r_selected += [execute_tournament(r_population[j * t_size:(j + 1) * t_size], self.p_sel)]
            else:
                r_selected += r_population
        return r_selected

    def make_selection(self, population):
        '''
        Given a population this function do the selection process:
        Select the k best individuals (elitism) and then fill the population wth a tournament selection

        :param population: population that needs to be selected
        :return: New population after the process of selection
        '''
        selected_population = [[]]*len(population)
        for i in range(len(population)): # For rach robot in the population
            if self.robots[i].establish_route:
                selected_population[i] = population[i]
                continue
            selected_population[i] = self.selection_operation(population[i])
        return selected_population

    def get_q_individuals(self):
        '''
        Method that get q individuals of each robot from the current population.

        :return: Selected q individuals of each robot in the population
        '''
        individuals = []
        for j in range(len(self.population)): # For each robot
            ind = []
            # Size of the groups to be evaluated by the tournament
            t_size = len(self.population[j]) // (self.q)
            for i in range(self.q):
                if i == self.q - 1: # i takes last value
                    # Not set finish index in order to avoid not using last element because population length may not be multiplot of q
                    ind += [execute_tournament(self.population[j][i * t_size:], self.p_eval)]
                else:
                    ind += [execute_tournament(self.population[j][i * t_size:(i + 1) * t_size], self.p_eval)]
            individuals += [ind] # Add selected solutions of this robot to results_old list
        return individuals

    def evaluate(self):
        '''
        Method that evaluates the current population. Takes the k first solutions of each robot and check its collisions.
        The result of the evaluation is the minimum number of collisions when checking all combinations of this k solutions.

        :return: Minimum number of collisions in the evaluation
        '''
        min_collisions = -1
        zero_collisions = None
        for i in range(len(self.population)): # For rach robot in the population
            max_length = max(list(map(lambda x: x.length, self.population[i])))
            self.population[i].sort(key=lambda x: x.get_sort_value(max_length))

        index = np.zeros(shape=len(self.population), dtype='i')
        end = False
        while not end:
            collisions = 0

            # Collect one route of each robot in order to test
            to_check = []
            for i in range(len(index)):
                to_check += [self.population[i][index[i]]]

            # Check if there is collision takeing one by one
            for i in range(len(to_check)):
                n_to_check = list(to_check)
                n_to_check.pop(i)
                for j in range(len(n_to_check)):
                    if have_collision(to_check[i].route, n_to_check[j].route):
                        collisions += 1

            # Test if new min collision
            if min_collisions == -1 or collisions < min_collisions:
                min_collisions = collisions
                if collisions == 0:
                    zero_collisions = list(to_check)

            # Update index
            index[0] += 1
            for i in range(len(index)):
                # Check if finish loop
                if index[i] == len(self.population[i]) or index[i] == self.k:
                    if i + 1 == len(index):
                        end = True
                        break
                    index[i] = 0
                    index[i+1] += 1
        return collisions, zero_collisions