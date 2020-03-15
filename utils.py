from math import sqrt
from random import shuffle, randint, uniform
import numpy as np
import matplotlib.pyplot as plt
from os import system

def inside_cluster(params, x, y):
    return 0 <= x < int(sqrt(params.CLUST_SIZE)) and 0 <= y < int(sqrt(params.CLUST_SIZE))


def success(probab):
    return probab > uniform(0,1)


def infect(population, params, cluster, x, y):
    if not(1 <= population[cluster, y, x] < params.INFECTION_TIME):
        return None

    neighbours = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]

    for n_x, n_y in neighbours:
        if inside_cluster(params, n_x, n_y) and success(params.INFECT_RATE):
            if population[cluster, n_y, n_x] == 0:
                population[cluster, n_y, n_x] = params.INFECTION_TIME
    return population


def proceed(population, param, cluster, x, y, active):
    if population[cluster, y, x] > 1:
        population[cluster, y, x] -= 1

        if success((param.DEATH_RATE + max(0, active - param.HEALTHCARE_CAPACITY)/param.HEALTHCARE_CAPACITY)
                /param.INFECTION_TIME):
            population[cluster, y, x] = -2

    elif population[cluster, y, x] == 1:
        population[cluster, y, x] = -1


def migration(population, params):
    def migration_condition(person):
        return person != -2
        # return not(person in range(params.INFECTION_TIME//5) or''' person == -2)

    for _ in range(params.MIGRATIONS_PER_DAY):
        first, second = randint(0,params.CLUSTERS-1), randint(0,params.CLUSTERS-1)
        x, y = (randint(0, int(sqrt(params.CLUST_SIZE))-1) for _ in range(2))

        if migration_condition(population[first, y, x]) and migration_condition(population[second, y, x]):
            population[first, y, x], population[second, y, x] = population[second, y, x], population[first, y, x]


def patients(population, params):
    active, healed, dead = 0, 0, 0
    for cluster in range(params.CLUSTERS):
        for y in range(int(sqrt(params.CLUST_SIZE))):
            for x in range(int(sqrt(params.CLUST_SIZE))):
                active += int(population[cluster, y, x] in tuple(range(1, params.INFECTION_TIME)))
                healed += int(population[cluster, y, x] == -1)
                dead += int(population[cluster, y, x] == -2)
    return active, healed+dead+active, healed, dead

def ill_rate(region, params):
    counter = 0
    for y in range(int(sqrt(params.CLUST_SIZE))):
        for x in range(int(sqrt(params.CLUST_SIZE))):
            counter += int(region[y,x] not in (0, -1))
    return counter / params.CLUST_SIZE

def frame_name(val, maxi):
    perc = str(int(100*val/maxi))
    perc = '0'*(3-len(perc))+perc
    return 'imgs/'+perc


def print_progressbar(val, maxi):
    perc = (100*val) // maxi
    system('clear')
    print('|'+('#'*(perc//10)) + (' '*(10 - perc//10)) + '|')
    print('|'+('#'*(perc%10)) + (' '*(10 - perc%10)) + '|')

def make_gif(name, run=True):
    print('creating a gif please wait ...')
    system('convert -delay 10 -loop 0 imgs/*.png imgs/'+name+'.gif')
    system('rm imgs/*.png')
    if run:
        system('mpv imgs/'+name+'.gif& disown')
        input('Naciśnij aby kontynuować ...')


def make_plot(params, cumulative, active, healed, dead, label, color):
    plt.close()
    color='red'
    label='pandemia'

    plt.plot(range(len(cumulative)), cumulative, c=color, label=label+' all')
    plt.plot(range(len(active)), active, c=color, label=label+' active', ls='--')
    plt.plot(range(len(dead)), dead, c=color, label=label+' deaths', ls=':')
    plt.plot(range(len(healed)), healed, c=color, label=label+' healed', ls='-.')
    plt.axhline(y=params.HEALTHCARE_CAPACITY, ls='dotted', c='black', label='healthcare capacity')
    plt.axhline(y=params.CLUSTERS*params.CLUST_SIZE, ls='dotted', c='green', label='population size')

    plt.legend()

