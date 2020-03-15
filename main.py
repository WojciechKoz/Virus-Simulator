from simulation import run_simulation
from parameters import Param
import matplotlib.pyplot as plt
from utils import make_gif, make_plot
from time import time

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


start = time()
cumulative, active, healed, dead = run_simulation(fst)
print('time elapsed:', time() - start) 
make_gif(NAME)

make_plot(fst, cumulative, active, healed, dead, label='', color='red')

plt.savefig('imgs/'+NAME+'.png')
plt.show()

