import math
import random
import matplotlib.pyplot as plt
import tsp_utils
import animated_visualizer


class SimulatedAnnealing:
    def __init__(self, coords, temp, alpha, stopping_temp, stopping_iter):
        ''' animate the solution over time

            Parameters
            ----------
            coords: array_like
                list of coordinates
            temp: float
                initial temperature
            alpha: float
                rate at which temp decreases
            stopping_temp: float
                temerature at which annealing process terminates
            stopping_iter: int
                interation at which annealing process terminates

        '''

        self.coords = coords
        self.sample_size = len(coords)
        self.temp = temp
        self.alpha = alpha
        self.stopping_temp = stopping_temp
        self.stopping_iter = stopping_iter
        self.iteration = 1

        self.dist_matrix = tsp_utils.vectorToDistMatrix(coords)
        self.curr_solution = tsp_utils.nearestNeighbourSolution(self.dist_matrix)
        self.best_solution = self.curr_solution

        self.solution_history = [self.curr_solution]

        self.curr_weight = self.weight(self.curr_solution)
        self.initial_weight = self.curr_weight
        self.min_weight = self.curr_weight

        self.weight_list = [self.curr_weight]

        self.acceptance_probability_list = []
        self.temperature_list = [self.temp]

        self.random_solution = tsp_utils.randomSolution(self.dist_matrix)
        self.random_weight = self.weight(self.random_solution)
        print
        print "Random: ", self.random_weight
        print
        print "Greedy: ", self.curr_weight
        print

    def weight(self, sol):

        return sum([self.dist_matrix[i, j] for i, j in zip(sol, sol[1:] + [sol[0]])])

    def acceptance_probability(self, candidate_weight):

        return math.exp(-abs(candidate_weight - self.curr_weight) / self.temp)

    def accept(self, candidate):

        candidate_weight = self.weight(candidate)
        if candidate_weight < self.curr_weight:

            self.curr_weight = candidate_weight
            self.curr_solution = candidate
            if candidate_weight < self.min_weight:
                print "updated length: %.9f    temperature: %.8f  "%(candidate_weight, self.temp)

                self.min_weight = candidate_weight
                self.best_solution = candidate

        else:
            self.acceptance_probability_list.append(self.acceptance_probability(candidate_weight))
            if random.random() < self.acceptance_probability(candidate_weight):
                self.curr_weight = candidate_weight
                self.curr_solution = candidate

    def anneal(self):
        '''
        Annealing process with 2-opt
        '''
        while self.temp >= self.stopping_temp and self.iteration < self.stopping_iter:
            candidate = list(self.curr_solution)
            l = random.randint(2, self.sample_size - 1)
            i = random.randint(0, self.sample_size - l)

            candidate[i: (i + l)] = reversed(candidate[i: (i + l)])

            self.accept(candidate)
            self.temp *= self.alpha
            self.iteration += 1
            self.weight_list.append(self.curr_weight)
            self.solution_history.append(self.curr_solution)
            self.temperature_list.append(self.temp)

        print
        print 'Random:                      ',self.random_weight                     
        print 'Greedy:                      ',self.initial_weight
        print '2-Opt + Simulated Annealing: ', self.min_weight
        print 'Improvement ratio on Random:           ', round((self.random_weight - self.min_weight) / (self.min_weight), 4) * 100, '%'
        print 'Improvement ratio on Greedy:           ', round((self.initial_weight - self.min_weight) / (self.min_weight), 4) * 100, '%'
        print

    def animateSolutions(self):
        animated_visualizer.animateTSP(self.solution_history, self.coords)

    def plotLearning(self):
        ap_length = len(self.acceptance_probability_list)
        new_list = []
        for i in range(0,ap_length):
            if i%20==0:
                new_list.append(self.acceptance_probability_list[i])

        plt.subplot(221)
        plt.plot([i for i in range(len(self.temperature_list))], self.temperature_list, c = 'b')
        plt.ylabel('Temperature')
        plt.xlabel('Iteration')

        plt.subplot(222)
        plt.axis([0,ap_length,-0.1,1.1])
        plt.scatter([i*20 for i in range(len(new_list))], new_list, marker = '.', c = 'k', s = 1)
        plt.ylabel('Acceptance probability')
        plt.xlabel('Sample Iteration')

        plt.subplot(212)
        plt.plot([i for i in range(len(self.weight_list))], self.weight_list, c = 'b')
        line_random = plt.axhline(y=self.random_weight, color='y', linestyle='--')
        line_init = plt.axhline(y=self.initial_weight, color='r', linestyle='--')
        line_min = plt.axhline(y=self.min_weight, color='g', linestyle='--')
        plt.legend([line_random, line_init, line_min], ['Random', 'Greedy', '2-Opt + Simulated Annealing'])
        plt.ylabel('Total length')
        plt.xlabel('Iteration')
        plt.show()
