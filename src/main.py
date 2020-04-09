from simulation import run_simulation
from parameters import Param
import matplotlib.pyplot as plt
from utils import make_gif, make_plot
from time import time
import sys

PATH = sys.argv[1] if len(sys.argv) == 2 else "../imgs/"
NAME = 'huge'

fst = Param(
    CLUSTERS = 12**2,
    CLUST_SIDE_LEN = 7,
    DAYS = 100,

    INFECTION_TIME = 20,
    DEATH_RATE = 0.4,
    INFECT_RATE = 0.3,
    MIGRATIONS_PER_DAY = 100,
    FEAR_RATE = 0.4,
    HEALTHCARE_CAPACITY = 2500
)


start = time()
cumulative, active, healed, dead, migrations, real_mig = run_simulation(fst, PATH)

print('time elapsed:', time() - start) 
make_gif(PATH, NAME)

# plt.plot(range(len(migrations)), migrations, label='migrations', color='blue')
plt.plot(range(len(real_mig)), real_mig, label='migrations', color='blue', ls=':')
make_plot(fst, cumulative, active, healed, dead, label='', color='red')

plt.savefig(PATH+NAME+'.png')

