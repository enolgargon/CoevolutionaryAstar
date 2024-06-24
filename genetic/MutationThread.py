import threading

class myThread (threading.Thread):
    def __init__(self, threadID, name, population, id, map, evaluation_individuals):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.population = population
        self.id = id

    def run(self):
        for j in range(len(self.population[self.id])):  # Solution by solution executes the mutation process
            s = Solution(mutate(self.population[self.id][j].route))
            s.calculate_fitness(self.map, evaluation_individuals)
            new_population[i] += [s]
