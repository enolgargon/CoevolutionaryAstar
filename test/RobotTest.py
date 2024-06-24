import unittest

from utilities import Robot, load_obstacle_matrix
from astar import search

class RobotTest(unittest.TestCase):

    def setUp(self):
        self.robots = []
        self.matrix = load_obstacle_matrix('F:\\MultirobotRouting\\scenery.txt')

        # Two robots that collision in same cell. Colision en (1,18)
        self.robots += [Robot([1,13], [1,23], self.matrix)]
        self.robots += [Robot([1,23], [1,13], self.matrix)]

        # Two robots that collision in crosscells. Colision entre (3,18) y (3,19)
        self.robots += [Robot([3,13], [3,24], self.matrix)]
        self.robots += [Robot([3,24], [3,13], self.matrix)]

        # Two robots for testing endind path colision
        self.robots += [Robot([2,7], [1,7], self.matrix)] # This one finish first
        self.robots += [Robot([1,3], [1,8], self.matrix)] # This one should go throw the endind cell of the other

    def test_collision_same_cell(self):
        # Search for the routes of robots
        for i in range(len(self.robots)):
            self.robots[i].set_route(search(self.robots[i].map, self.robots[i].start_point, self.robots[i].end_point))

        # Check this type of collision
        self.assertEqual(self.robots[0].colision_with(self.robots[1]), (1, 18))
        self.assertEqual(self.robots[1].colision_with(self.robots[0]), (1, 18))

        # Check no other collisions with this robots
        for i in range(2, len(self.robots)):
            self.assertEqual(self.robots[0].colision_with(self.robots[i]), None)
            self.assertEqual(self.robots[i].colision_with(self.robots[0]), None)
            self.assertEqual(self.robots[1].colision_with(self.robots[i]), None)
            self.assertEqual(self.robots[i].colision_with(self.robots[1]), None)

    def test_collision_crosscells(self):
        # Search for the routes of robots
        for i in range(len(self.robots)):
            self.robots[i].set_route(search(self.robots[i].map, self.robots[i].start_point, self.robots[i].end_point))

        # Check this type of collision
        self.assertEqual(self.robots[2].colision_with(self.robots[3]), (3, 19))
        self.assertEqual(self.robots[3].colision_with(self.robots[2]), (3, 18))

        # Check no other collisions with this robots
        for i in range(0, len(self.robots)):
            if i == 2 or i == 3:
                continue
            self.assertEqual(self.robots[2].colision_with(self.robots[i]), None)
            self.assertEqual(self.robots[i].colision_with(self.robots[2]), None)
            self.assertEqual(self.robots[3].colision_with(self.robots[i]), None)
            self.assertEqual(self.robots[i].colision_with(self.robots[3]), None)

    def test_collision_end_path(self):
        # Search for the routes of robots
        for i in range(len(self.robots)):
            self.robots[i].set_route(search(self.robots[i].map, self.robots[i].start_point, self.robots[i].end_point))

        # Check this type of collision
        self.assertEqual(self.robots[4].colision_with(self.robots[5]), None)
        self.assertEqual(self.robots[5].colision_with(self.robots[4]), (1, 7))

        # Check no other collisions with this robots
        for i in range(0, len(self.robots)):
            if i == 4 or i == 5:
                continue
            self.assertEqual(self.robots[4].colision_with(self.robots[i]), None)
            self.assertEqual(self.robots[i].colision_with(self.robots[4]), None)
            self.assertEqual(self.robots[5].colision_with(self.robots[i]), None)
            self.assertEqual(self.robots[i].colision_with(self.robots[5]), None)

    def test_place_obstacle(self):
        x = 18
        y = 5
        # Check position without obstacle anywhere
        for i in range(len(self.robots)):
            self.assertEqual(self.robots[i].map[y,x], 0)
        self.assertEqual(self.matrix[y][x], 0)

        # Place an obstacle in first robot and check it
        self.robots[0].place_obstacle((x,y))
        self.assertEqual(self.robots[0].map[y,x], 1)

        # Check other robots without obstacle in this position
        for i in range(1, len(self.robots)):
            self.assertEqual(self.robots[i].map[y,x], 0)
        self.assertEqual(self.matrix[y][x], 0)

    def test_no_routes_calculated_before_check_obstacles(self):
        # No routes calculated
        with self.assertRaises(Exception):
            self.robots[0].colision_with(self.robots[1])
        with self.assertRaises(Exception):
            self.robots[1].colision_with(self.robots[0])
        with self.assertRaises(Exception):
            self.robots[2].colision_with(self.robots[3])
        with self.assertRaises(Exception):
            self.robots[3].colision_with(self.robots[2])
        with self.assertRaises(Exception):
            self.robots[4].colision_with(self.robots[5])
        with self.assertRaises(Exception):
            self.robots[5].colision_with(self.robots[4])

        # Only even routes calculated
        for i in range(len(self.robots), 2):
            self.robots[i].route = search(self.robots[i].map, self.robots[i].start_point, self.robots[i].end_point)

        with self.assertRaises(Exception):
            self.robots[0].colision_with(self.robots[1])
        with self.assertRaises(Exception):
            self.robots[1].colision_with(self.robots[0])
        with self.assertRaises(Exception):
            self.robots[2].colision_with(self.robots[3])
        with self.assertRaises(Exception):
            self.robots[3].colision_with(self.robots[2])
        with self.assertRaises(Exception):
            self.robots[4].colision_with(self.robots[5])
        with self.assertRaises(Exception):
            self.robots[5].colision_with(self.robots[4])

        # All routes calculated. No exceptions
        for i in range(len(self.robots)):
            self.robots[i].route = search(self.robots[i].map, self.robots[i].start_point, self.robots[i].end_point)

        self.robots[0].colision_with(self.robots[1])
        self.robots[1].colision_with(self.robots[0])
        self.robots[2].colision_with(self.robots[3])
        self.robots[3].colision_with(self.robots[2])
        self.robots[4].colision_with(self.robots[5])
        self.robots[5].colision_with(self.robots[4])

if __name__ == '__main__':
    unittest.main()