import numpy as np
import matplotlib.pyplot as plt
from random import shuffle, randint, uniform
from math import sqrt
from utils import infect, proceed, migration, patients, ill_rate, frame_name, print_progressbar
import seaborn as sns


def make_heatmap(params, X, day):
    world = np.array([ill_rate(mat, params) 
        for mat in X]).reshape((int(sqrt(params.CLUSTERS)),int(sqrt(params.CLUSTERS))))

    sns.heatmap(world, cmap='Greys', vmin=0, vmax=1)
    plt.savefig(frame_name(day, params.DAYS)+' day.png')
    plt.close()


def update_stats(human, cumul, actv, heald, dead):
    if human == 0:
        return cumul, actv, heald, dead
    if human == -1:
        return cumul+1, actv, heald+1, dead
    if human == -2:
        return cumul+1, actv, heald, dead+1
    return cumul+1, actv+1, heald, dead


def day_update(params, X, active):
    cumulative_num, active_num, healed_num, dead_num = (0,0,0,0)
    for cluster in range(params.CLUSTERS):
        for y in range(int(sqrt(params.CLUST_SIZE))):
            for x in range(int(sqrt(params.CLUST_SIZE))):
                infect(X, params, cluster, x, y)
                proceed(X, params, cluster, x, y, active[-1])

                # update numbers of healed, dead etc 
                cumulative_num, active_num, healed_num, dead_num = \
                        update_stats(X[cluster, y, x], \
                                cumulative_num, active_num, healed_num, dead_num)

    migration(X, params)
    return cumulative_num, active_num, healed_num, dead_num


def run_simulation(params):

    '''
    X - 3D matrix representing a world 
    each single number in that matrix is a human
    value of these numbers correspond to current health condition of people
    you can read more about it in README 
    '''
    X = np.zeros((params.CLUSTERS, int(sqrt(params.CLUST_SIZE)), int(sqrt(params.CLUST_SIZE))))

    # first ill people
    for _ in range(10): # TODO constant or parameter ?
        X[randint(0,params.CLUSTERS-1), \
                randint(0,int(sqrt(params.CLUST_SIZE)-1)), randint(0,int(sqrt(params.CLUST_SIZE)-1))] = 1

    # outputs of simulation
    cumulative = [0]
    active = [0]
    healed = [0]
    dead = [0]

    for day in range(params.DAYS):
        print_progressbar(day, params.DAYS) 
        make_heatmap(params, X, day)

        # simulate a single day
        cumul_num ,patients_num, healed_num, dead_num = day_update(params, X, active)

        # change rate of migration
        delta = patients_num - active[-1]
        params.MIGRATIONS_PER_DAY -= int(delta*params.FEAR_RATE/params.MIGRATIONS_PER_DAY)
        params.MIGRATIONS_PER_DAY = max(1, params.MIGRATIONS_PER_DAY)

        # save all daily data
        cumulative.append(cumul_num)
        active.append(patients_num)
        healed.append(healed_num)
        dead.append(dead_num)

    return cumulative, active, healed, dead
