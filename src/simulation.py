import numpy as np
import matplotlib.pyplot as plt
from random import shuffle, randint, uniform
from simulation_utils import infect, proceed, migration, ill_rate
from utils import frame_name
import seaborn as sns
from math import sqrt
from tqdm import tqdm
import sys


def make_heatmap(params, X, day, path):
    world = np.array([ill_rate(mat, params) 
        for mat in X]).reshape((int(sqrt(params.CLUSTERS)),int(sqrt(params.CLUSTERS))))

    ax = plt.axes()
    sns.heatmap(world, cmap='Greys', vmin=0, vmax=1)
    ax.set_title("active cases. Day "+str(day))
    plt.savefig(frame_name(day, params.DAYS, path)+' day.png')
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
        for y in range(params.CLUST_SIDE_LEN):
            for x in range(params.CLUST_SIDE_LEN):
                infect(X, params, cluster, x, y)
                proceed(X, params, cluster, x, y, active[-1])

                # update numbers of healed, dead etc 
                cumulative_num, active_num, healed_num, dead_num = \
                        update_stats(X[cluster, y, x], \
                                cumulative_num, active_num, healed_num, dead_num)

    mig_num = migration(X, params)
    return cumulative_num, active_num, healed_num, dead_num, mig_num


def run_simulation(params, path):
    '''
    X - 3D matrix representing a world 
    each single number in that matrix is a human
    value of these numbers correspond to current health condition of people
    you can read more about it in README 
    '''
    X = np.zeros((params.CLUSTERS, params.CLUST_SIDE_LEN,params.CLUST_SIDE_LEN))

    # first ill people
    for _ in range(10): # TODO constant or parameter ?
        X[randint(0,params.CLUSTERS-1), \
                randint(0,params.CLUST_SIDE_LEN-1), randint(0,params.CLUST_SIDE_LEN-1)] = \
                params.INFECTION_TIME

    # outputs of simulation
    cumulative = [0]
    active = [0]
    healed = [0]
    dead = [0]
    migrations = [params.MIGRATIONS_PER_DAY]
    real_mig = [params.MIGRATIONS_PER_DAY]

    bar = tqdm(total=params.DAYS, file=sys.stdout)
    for day in range(params.DAYS):
        bar.update(1)
        make_heatmap(params, X, day, path)

        # simulate a single day
        cumul_num, patients_num, healed_num, dead_num, real_mig_num = day_update(params, X, active)

        # change rate of migration
        if len(active) > params.INFECTION_TIME//2:
            delta = active[-params.INFECTION_TIME//2 + 1] - active[-params.INFECTION_TIME//2]
            params.MIGRATIONS_PER_DAY -= int(delta*params.FEAR_RATE)
            params.MIGRATIONS_PER_DAY = max(1, params.MIGRATIONS_PER_DAY)

        # save all daily data
        cumulative.append(cumul_num)
        active.append(patients_num)
        healed.append(healed_num)
        dead.append(dead_num)
        migrations.append(params.MIGRATIONS_PER_DAY)
        real_mig.append(real_mig_num)

    bar.close()
    return cumulative, active, healed, dead, migrations, real_mig
