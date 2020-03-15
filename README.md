# Virus-Simulator
Virus simulator written in python

## Requirements
+ python 3.7.6
+ matplotlib 3.2.0
+ numpy 1.15.0
+ seaborn 0.10.0
+ linux and imagemagick (optional for "live" visualization)

## Usage examples

## TODO
[ ] People migrate less when they at the second half of their illness
[ ] People can become ill twice (but with less probability)
[ ] Divide world to countries (people go abroad less frequently)
[ ] Each country has own health care
[ ] Full support for Windows
[ ] add GUI

## Implementation details
### run_simulation - population
3D matrix representing a world.
Each single number in that matrix is a human.
Value of these numbers correspond to 
current health condition of people.
Human can be:

+ 0 - healthy
+ -1 - recovered (and now has disease resistance)
+ -2 - dead
+ from 1 to params.INFECTION_TIME - ill

People can infect each other when they are close.

population[z,y,x] can infect only:

1. population[z,y+1,x]
2. population[z,y-1,x]
3. population[z,y,x+1]
4. population[z,y,x-1]

z axis is like a list of cities. People can migrate from
one city to another and (when they are ill) bring virus 
to the next city.
