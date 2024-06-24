import argparse
import sys
from argparse import RawTextHelpFormatter
import time

from astar import search
from genetic import GeneticAlgorithm
from utilities import answer_for_robot_coordinates, load_obstacle_matrix, Robot, show_map, load_robot_coordinates, show_routes

pars = argparse.ArgumentParser(
    description="Routing calculator using algorithm A* and a proprietary coevolutionary algorithm",
    formatter_class=RawTextHelpFormatter)

pars.add_argument('filename', metavar='filename', type=str, nargs='?', help='Path of the file containing the information about the start and destination points of the robots.')
pars.add_argument('-scenery', type=str, default='scenery.txt', help='Route for the scenery file')
pars.add_argument('-n_robots', type=int, default=3, help='Number of robots in route calculation')
pars.add_argument('-n_a', type=int, default=3, help='Number of iterations to be performed of algorithm A*')
pars.add_argument('-n_gen', type=int, default=100, help='Number of running generations of the coevolutionary algorithm')

pars.add_argument('-p_size', type=int, default=9, help='Size of the population of solutions when running the coevolutionary algorithm')
pars.add_argument('-q', type=int, default=1, help='Q. Number of solutions from other robots to be used to evaluate the performance of a robot.')
pars.add_argument('-p_eval', type=float, default=0.5, help='Probability of selection in the tournament held to select the Q individuals to be evaluated')
pars.add_argument('-k', type=int, default=3, help='K. Elitism, number of best individuals maintained between generations.')
pars.add_argument('-p_sel', type=float, default=0.35, help='Probability of selection in the tournament that takes place in the selection stage')

args = pars.parse_args()

n_robots = args.n_robots
n_a = args.n_a
n_gen = args.n_gen

p_size = args.p_size
q = args.q
p_eval = args.p_eval
k = args.k
p_sel = args.p_sel

matrix = load_obstacle_matrix(args.scenery)
if args.filename is None:
    coordinates = answer_for_robot_coordinates(n_robots)
else:
    coordinates = load_robot_coordinates(args.filename)
    n_robots = len(coordinates)

robots = []
for r in coordinates:
    robots += [Robot(r[0], r[1], matrix)]
start = time.time()

for robot in robots:
    robot.set_route(search(robot.map, robot.start_point, robot.end_point))
    print(robot)

for i in range(n_a):
    print(f"Iter {i}")
    collision = False
    for a in range(n_robots):
        individual_collision = False
        for b in range(n_robots):
            if robots[a].establish_route or a == b:
                continue
            print(a, b)
            collision_pos = robots[a].colision_with(robots[b])
            if collision_pos is not None:
                print(collision_pos)
                collision = True
                individual_collision = True
                robots[a].place_obstacle((collision_pos[1], collision_pos[0]))
                r = search(robots[a].map, robots[a].start_point, robots[a].end_point, max_iterations=15000)
                if r is not None:
                    robots[a].set_route(r)
        if not individual_collision:
            robots[a].establish_route = True

    if not collision:
        print(f"Solution found by A* in {i} iteration")
        for i in range(n_robots):
            print(f"Robot {i}", robots[i].route)
        for i in range(n_robots):
            print(len(robots[i].route[0]))
        show_map(matrix, robots)
        end = time.time()
        print(f"Execution time: {end-start}")
        sys.exit(0)

change = time.time()
ga = GeneticAlgorithm(robots, matrix, p_size=p_size, q=q, p_eval=p_eval, k=k, p_sel=p_sel)
c, r = ga.evaluate()
print(f"Generation 0/{n_gen}. # collisions in evaluation: {c}")
for i in range(n_gen):
    c, r = ga.make_iteration()
    print(f"Generation {i + 1}/{n_gen}. # collisions in evaluation: {c}")
    if c == 0:
        print(f"Solution found by Coevolutionary Algorithm in {i} generation")
        if r is not None:
            to_draw = []
            for j in range(len(r)):
                route = r[j].route
                to_draw += [route]
                print(f"Robot {j}: ", route)
            print("Robot times:")
            for j in range(len(r)):
                print(len(r[j].route[0]))
            show_routes(matrix, to_draw)
        else:
            for j in range(n_robots):
                print(f"Routes for robot {k}")
                for k in range(min(len(ga.population[j]), ga.k)):
                    print(ga.population[j][k].route)
        end = time.time()
        print(f"Execution time: {end-start}")
        print(f"A* time: {change - start}")
        print(f"Coevolutive time: {end - change}")
        sys.exit(0)
print("No solution found")

end = time.time()
print(f"Execution time: {end-start}")
print(f"A* time: {change - start}")
print(f"Coevolutive time: {end - change}")
