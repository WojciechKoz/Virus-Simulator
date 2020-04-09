from random import shuffle, randint, uniform

def inside_cluster(params, x, y):
    return 0 <= x < params.CLUST_SIDE_LEN and 0 <= y < params.CLUST_SIDE_LEN


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
        return not (0 < person <= params.INFECTION_TIME//2 or person == -2)

    counter = 0
    for _ in range(params.MIGRATIONS_PER_DAY):
        first, second = randint(0,params.CLUSTERS-1), randint(0,params.CLUSTERS-1)
        x, y = (randint(0, params.CLUST_SIDE_LEN-1) for _ in range(2))

        if migration_condition(population[first, y, x]) and migration_condition(population[second, y, x]):
            population[first, y, x], population[second, y, x] = population[second, y, x], population[first, y, x]
            counter += 1
    return counter


def ill_rate(region, params):
    counter = 0
    for y in range(params.CLUST_SIDE_LEN):
        for x in range(params.CLUST_SIDE_LEN):
            counter += int(region[y,x] not in (0, -1))
    return counter / params.CLUST_SIDE_LEN**2
