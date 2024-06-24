import unittest

from astar import search
from genetic import mutate, fitness
from utilities import Robot, load_obstacle_matrix, show_map, show_routes


class GeneticAlgorithmTest(unittest.TestCase):
    def setUp(self):
        self.matrix = load_obstacle_matrix('F:\\MultirobotRouting\\scenery.txt')
        self.robot_1 = Robot([8, 10], [3, 19], self.matrix)
        self.robot_1.set_route(search(self.robot_1.map, self.robot_1.start_point, self.robot_1.end_point))

    def test_visual(self):
        nr = mutate(self.robot_1.route)

        print(self.robot_1.route)
        print(nr)

        #show_map(self.matrix, [self.robot_1])
        show_routes(self.matrix, [self.robot_1.route, nr])

    def test_mutate(self):
        r = self.robot_1.route
        for i in range(50):
            print(i)
            r = mutate(r)
            self.assertEqual(list(self.robot_1.start_point), list(r[1][0]))
            self.assertEqual(list(self.robot_1.end_point), list(r[1][-1]))

    def test_fitness(self):
        other_routes = [('UUUL', [(8, 16), (7, 16), (6, 16), (5, 16), (5, 15)]), ('LLLLLLLLLDDLLULLDLLU',
                                                                                  [(5, 27), (5, 26), (5, 25), (5, 24),
                                                                                   (5, 23), (5, 22), (5, 21), (5, 20),
                                                                                   (5, 19), (5, 18), (6, 18), (7, 18),
                                                                                   (7, 17), (7, 16), (6, 16), (6, 15),
                                                                                   (6, 14), (7, 14), (7, 13), (7, 12),
                                                                                   (6, 12)])]

        # Route with obstacle and no other routes
        r = ('RRRRRUURDRDRRUUUUU',
             [(8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (7, 15), (6, 15), (6, 16), (7, 16), (7, 17),
              (8, 17), (8, 18), (8, 19), (7, 19), (6, 19), (5, 19), (4, 19), (3, 19)])
        self.assertEqual(1000000, fitness(r, self.matrix))

        # Route with obstacle and other routes without collision. Same r that before
        self.assertEqual(1000000, fitness(r, self.matrix, other_routes))

        # Route with obstacle and other routes with collision
        r = ('RRRRRUURDRRUUUUR',
             [(8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (7, 15), (6, 15), (6, 16), (7, 16), (7, 17),
              (7, 18), (6, 18), (5, 18), (4, 18), (3, 18), (3, 19)])
        self.assertEqual(1000000, fitness(r, self.matrix, other_routes))

        # Route without obstacles and no other routes
        r = ('RRRRUURRDRDRRUUUUU',
             [(8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (7, 14), (6, 14), (6, 15), (6, 16), (7, 16), (7, 17),
              (8, 17), (8, 18), (8, 19), (7, 19), (6, 19), (5, 19), (4, 19), (3, 19)])
        self.assertEqual(len(r[0]), fitness(r, self.matrix))

        # Route without obstacles and other routes without collision. Same r that test before
        self.assertEqual(len(r[0]), fitness(r, self.matrix, other_routes))

        # Route without obstacles and other routes with collision
        r = ('RRRRUURRDRRUUUUR',
             [(8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (7, 14), (6, 14), (6, 15), (6, 16), (7, 16), (7, 17),
              (7, 18), (6, 18), (5, 18), (4, 18), (3, 18), (3, 19)])
        self.assertEqual(len(r[0]) + 1, fitness(r, self.matrix, other_routes))

        pass


if __name__ == '__main__':
    unittest.main()
