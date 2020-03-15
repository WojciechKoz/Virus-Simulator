import numpy as np
import matplotlib.pyplot as plt
from random import shuffle, randint, uniform
from math import sqrt
from utils import infect, proceed, migration, patients, ill_rate, frame_name, print_progressbar
import seaborn as sns

def run_simulation(params):
    # at the beginning all guys are healthy
    X = np.zeros((params.CLUSTERS, int(sqrt(params.CLUST_SIZE)), int(sqrt(params.CLUST_SIZE))))

    # first ill people
    for _ in range(10): # TODO constant or parameter ?
        X[randint(0,params.CLUSTERS-1), \
                randint(0,int(sqrt(params.CLUST_SIZE)-1)), randint(0,int(sqrt(params.CLUST_SIZE)-1))] = 1

    # outputs of simulation
    cumulative = []
    active = []
    healed = []
    dead = []

    for epoch in range(params.DAYS):
        print_progressbar(epoch, params.DAYS)
        world = np.array([ill_rate(mat, params) 
            for mat in X]).reshape((int(sqrt(params.CLUSTERS)),int(sqrt(params.CLUSTERS))))

        sns.heatmap(world, cmap='Greys', vmin=0, vmax=1)
        plt.savefig(frame_name(epoch, params.DAYS)+' day.png')
        plt.close()

        for cluster in range(params.CLUSTERS):
            for y in range(int(sqrt(params.CLUST_SIZE))):
                for x in range(int(sqrt(params.CLUST_SIZE))):
                    infect(X, params, cluster, x, y)
                    proceed(X, params, cluster, x, y, active[-1] if active else 0)
        migration(X, params)
        patients_num, cumul_num, healed_num, dead_num = patients(X, params)

        if active:
            delta = patients_num - active[-1]
            params.MIGRATIONS_PER_DAY -= int(delta*params.FEAR_RATE/params.MIGRATIONS_PER_DAY)
            params.MIGRATIONS_PER_DAY = max(1, params.MIGRATIONS_PER_DAY)

        cumulative.append(cumul_num)
        active.append(patients_num)
        healed.append(healed_num)
        dead.append(dead_num)

    return cumulative, active, healed, dead
