from simulation import run_simulation
from parameters import Param
import matplotlib.pyplot as plt
from utils import make_gif, make_plot

NAME = 'normal'

fst = Param(
    CLUSTERS = 144,
    CLUST_SIZE = 100,
    DAYS = 200,
    INFECTION_TIME = 30,
    DEATH_RATE = 0.3,
    INFECT_RATE = 0.4,
    MIGRATIONS_PER_DAY = 30,
    FEAR_RATE = 0.1,
    HEALTHCARE_CAPACITY = 2000
)


cumulative, active, healed, dead = run_simulation(fst)
make_gif(NAME)

make_plot(fst, cumulative, active, healed, dead, label='pandemia', color='red')

plt.savefig('imgs/'+NAME+'.png')
plt.show()

'''
run_simulation(ax, sec, 'red', 'sec')

'''
