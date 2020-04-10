from os import system
from sys import platform
import matplotlib.pyplot as plt

def clear():
    if platform[:3] == 'win':
        system('cls')
    elif platform[:3] == 'lin':
        system('clear')


def frame_name(val, maxi, path):
    zeros = len(str(maxi)) - len(str(val))
    return path+"0"*zeros+str(val)


def make_gif(path, name, run=True):
    if platform[:3] != 'lin': 
        print("Sorry, I can't make a gif on Windows")
        return None

    print('creating a gif please wait ...', flush=True)
    system('convert -delay 10 -loop 0 '+path+'*day.png '+path+name+'.gif')
    system('rm '+path+'*day.png')


def make_plot(params, cumulative, active, healed, dead, label, color):
    plt.plot(range(len(cumulative)), cumulative, c=color, label=label+' all')
    plt.plot(range(len(active)), active, c=color, label=label+' active', ls='--')
    plt.plot(range(len(dead)), dead, c=color, label=label+' deaths', ls=':')
    plt.plot(range(len(healed)), healed, c=color, label=label+' healed', ls='-.')
    plt.axhline(y=params.HEALTHCARE_CAPACITY, ls='dotted', c='black', label='healthcare capacity')
    plt.axhline(y=params.CLUSTERS*params.CLUST_SIDE_LEN**2, ls='dotted', c='green', label='population size')

    plt.legend()

