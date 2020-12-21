import numpy as np
import random
import yaml

import matplotlib.pyplot as plt




with open('Config.yaml') as d:
    data = yaml.load(d, Loader=yaml.FullLoader)

    logs = data['logs']
    evals = data['evaluations']
    problem_instance_pathname = data['problem_instance_pathname']
    solution_file_pathname = data['solution_file_pathname']
    random.seed(data['random_seed'])
    log_file_pathname = data['log_file_pathname']

    l = open(log_file_pathname, "w+")
    l.write('Result Log' + '\n')

    l.write('\n' + 'Logs: \t' + str(data['logs']))
    l.write('\n' + 'Evaluations:  \t' + str(data['evaluations']))
    l.write('\n' + 'Random seed: \t' + str(data['random_seed']))
    l.write('\n' + 'Log file path+name: \t' + str(data['log_file_pathname']))
    l.write('\n' + 'Solution file path+name: \t' + str(data['solution_file_pathname']) + '\n')

# solution file
o = open(solution_file_pathname, "w+")
# input file
with open(problem_instance_pathname) as f:
    # line = f.readline()
    cnt = 1
    # while line:
    # print("Line {}: {}".format(cnt, line.strip()))

    frl = f.readline()
    x = int(frl)
    o.write(frl)

    frl = f.readline()
    y = int(frl)
    o.write(frl)

    print(int(x))
    print(y)

    # Initializing a board in which 0 represents
    # an empty cell and 1 represents a lamp
    board = np.zeros([int(x), int(y)])

    # Saving the positions of the black cells in
    # bc_board in which 0 represents an empty cell
    # and 2 represents a black cell
    bc_board = np.zeros_like(board)

    # Reading the input file
    line = f.readline()
    o.write(line)

    while line:
        xyz = line.split()
        xi = int(xyz[0])
        yi = int(xyz[1])
        zi = int(xyz[2])

        board[xi - 1, yi - 1] = 1
        bc_board[xi - 1, yi - 1] = zi
        # print(xyz, xi, yi, zi)
        line = f.readline()
        o.write(line)

# print(a)
# print(b)

# counting the number of the black cells
bc = board.sum()
# counting the number of the white cells
wc = x * y - bc

print('wc', wc, 'bc', bc)


# A list for saving each log's best solution
log_sol = []
# A list for saving each log's best fitness
log_fit = np.zeros([logs])



# the fittest solution of all in an experiment
max_fit = 0

for i in range(logs):

    print('log:' + str(i))
    best_fitness = 0
    fitness_hist = np.zeros([evals + 1])  # fitness history for plotting
    sol_hist = []  # for saving the best solutions so far at each run
    c = 0

    # for k in range(evals):
    k = 0

    l.write('\n' + 'Run' + str(i))

    while k < evals:

        # k += 1
        # generating a uniform number for the number of lamps
        random_lamps = random.randint(0, wc)
        # print('random_lamps', random_lamps)
        # for random bulb placement
        random_board = board.copy() * 2
        # the lightened area
        lightened = board.copy()
        lightened *= 2
        # print('board:')
        # print(board)

        valid = 1
        fitness = 0

        # print(k)
        # counter of placed bulbs
        j = 0
        while j < random_lamps:

            r1 = random.randint(0, x - 1)
            r2 = random.randint(0, y - 1)

            if random_board[r1, r2] == 0:

                # print('New lamp at:', r1, r2)
                # lamp cells are marked with 2
                random_board[r1, r2] = 7
                j += 1
                # updating the lightened area
                s = r1 + 1
                t = r2

                while s < x and board[s][r2] != 1:

                    if random_board[s][r2] == 7:

                        valid = 0
                        fitness = 0
                        # print('The new lamp lightens cell:', s, r2)
                        j = random_lamps

                    else:
                        if lightened[s][r2] == 0:
                            fitness += 1
                        lightened[s][r2] = 1
                    s += 1

                s = r1 - 1

                while s > -1 and board[s][r2] != 1:

                    if random_board[s][r2] == 7:

                        valid = 0
                        fitness = 0
                        # print('The new lamp lightens cell:', s, r2)
                        j = random_lamps
                    else:
                        if lightened[s][r2] == 0:
                            fitness += 1
                        lightened[s][r2] = 1

                    s -= 1

                s = r1
                t = r2 + 1

                while t < y and board[r1][t] != 1:

                    if random_board[r1][t] == 7:

                        valid = 0
                        fitness = 0
                        # print('The new lamp lightens cell:', r1, t)
                        # break
                        j = random_lamps
                    else:
                        if lightened[r1][t] == 0:
                            fitness += 1
                        lightened[r1][t] = 1

                    t += 1

                t = r2 - 1

                while t > -1 and board[r1][t] != 1:

                    if random_board[r1][t] == 7:

                        valid = 0
                        fitness = 0
                        # print('The new lamp lightens cell:', r1, t)
                        j = random_lamps
                    else:
                        if lightened[r1][t] == 0:
                            fitness += 1
                        lightened[r1][t] = 1

                    t -= 1

                t = r2
                # marking the lamps with 7 in
                # lightened matrix
                lightened[r1][r2] = 7
                fitness += 1
                # print(lightened)
        # setting the fitness of the invalid solutions to 0
        if valid == 0:
            fitness = 0

        if fitness > best_fitness:
            # print('this')
            # print(fitness, best_fitness)
            # print(lightened)
            best_fitness = fitness
            fitness_hist[k] = fitness
            sol_hist.append(lightened)
            c += 1
            l.writelines(['\n' + str(k) + '\t' + str(fitness), ' '])
            # print('fitness', fitness)
            if fitness > max_fit:
                max_fit = fitness
                max_sol = lightened.copy()

        if valid != 0:
            k += 1
    l.write('\n')
    if len(sol_hist) > 0:
        log_sol.append(sol_hist.pop())
    log_fit[i] = best_fitness

    # print(random_board)

# visualize(random_board)
# visualize(lightened)
# print('random_board_final')
# print(random_board)
# print('lightened_final')
# print(lightened)
# print('valid:', valid)
# print('sol_hist')
# print('len(sol_hist)', len(sol_hist))
# print(sol_hist.pop())
# print('c', c)
# print('best_fitness', best_fitness)
# for i in sol_hist:
# print(i)
# sol = sol_hist.pop()
# print(sol_hist.pop())
# print(sol)
# o = open('solution.txt', "w+")
o.writelines(['\n'])

o.writelines(str(max_fit))
for i in range(x):
    for j in range(y):
        if max_sol[i][j] == 7:
            o.writelines(' ')
            o.writelines(['\n' + str(i + 1) + ' ' + str(j + 1), ' '])

# print(len(fitness_hist))
# print(fitness_hist)
# a=np.zeros([10])
# print('a',a)
plt.plot(fitness_hist,'.')
plt.show()
# visualize(lightened)
# print(i, random_board)
# print(log_sol)
# print(log_fit)
# print(max_sol)
