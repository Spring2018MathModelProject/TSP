import numpy as np
from nodes_generator import NodeGenerator
from simulated_annealing import SimulatedAnnealing


def main():
    '''set the simulated annealing algorithm params'''
    temp = 1000
    stopping_temp = 0.00000001
    alpha = 0.9995
    stopping_iter = 10000000

    '''set the dimensions of the grid'''
    size_width = 50
    size_height = 50

    '''set the number of nodes'''
    population_size = 100

    '''generate random list of nodes'''
    '''nodes = NodeGenerator(size_width, size_height, population_size).generate()'''
    f = open('data.txt')
    xs = []
    ys = []
    for data in f.readlines():
        data = data.strip('\n')
        nums = data.split(" ")
        while '' in nums:
            nums.remove('')
        xs.append(int(nums[0]))
        ys.append(int(nums[1]))
    nodes = np.column_stack((xs, ys))
    f.close()

    '''run simulated annealing algorithm with 2-opt'''
    sa = SimulatedAnnealing(nodes, temp, alpha, stopping_temp, stopping_iter)
    sa.anneal()

    '''animate'''
    sa.animateSolutions()

    '''show the improvement over time'''
    sa.plotLearning()


if __name__ == "__main__":
    main()
