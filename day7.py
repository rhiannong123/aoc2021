import pandas as pd
import numpy as np
import datetime


import advent_of_code as aoc

## Read in input
num = 7
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = True




## Functions ##################################################


def fuel_consumption(crabs,horiz_guess):
    '''Assumes one-to-one ratio of horizontal movement and fuel
       1 space = 1 fuel unit,
       2 spaces = 2 fuel units... 
    '''
    fuel = [abs(icrab - horiz_guess) for icrab in crabs]

    return sum(fuel), fuel

def fuel_consumption2(crabs,horiz_guess):
    '''1 space = 1 fuel unit,
       2 spaces = 3 fuel units,
       3 spaces = 6 fuel units,
       4 spaces = 10 fuel units ...
    '''
    horiz_changes = [abs(icrab - horiz_guess) for icrab in crabs]
    fuel = [sum(range(i+1)) for i in horiz_changes]
    
    return sum(fuel), fuel




## PART 1  ##################################################

crabs = [int(crab) for crab in lines[0].split(',')]

## Start with average of crabs as guess
## Iterate up or down, which ever way makes the fuel consumption less
## In this way, find the minimum fuel consumption
guess = int(np.average(crabs))

stop = 0
while stop == 0:
    fuel = fuel_consumption(crabs,guess)[0]

    if verbose:
        print('current guess, current fuel: ', guess, fuel)

    ## Check if incrementing horizontal guess by +1 is more or less fuel
    fuel_incr_pos = fuel_consumption(crabs,guess + 1)[0]
    if fuel < fuel_incr_pos:
        ## CASE current horizontal guess uses less fuel than one guess higher
        ##  try one lower
        fuel_incr_neg = fuel_consumption(crabs,guess - 1)[0]

        if fuel < fuel_incr_neg:
            ## CASE found lowest fuel usage! Exit while loop
            lowest_fuel = fuel
            horizontal_pos = guess
            stop = 1
        else:
            ## CASE neg incr uses less fuel than current guess
            ##  head that direction
            guess -= 1
    else:
        ## CASE pos incr uses less fuel than current guess
        ##  head that direction
        guess += 1
            
print(f'Answer: {lowest_fuel}')




## PART 2  ##################################################

crabs = [int(crab) for crab in lines[0].split(',')]

## Start with average of crabs as guess
## Iterate up or down, which ever way makes the fuel consumption less
## In this way, find the minimum fuel consumption
## Update to use second fuel consumption function!
guess = int(np.average(crabs))

stop = 0
while stop == 0:
    fuel = fuel_consumption2(crabs,guess)[0]

    if verbose:
        print('current guess, current fuel: ', guess, fuel)

    ## Check if incrementing horizontal guess by +1 is more or less fuel
    fuel_incr_pos = fuel_consumption2(crabs,guess + 1)[0]
    if fuel < fuel_incr_pos:
        ## CASE current horizontal guess uses less fuel than one guess higher
        ##  try one lower
        fuel_incr_neg = fuel_consumption2(crabs,guess - 1)[0]

        if fuel < fuel_incr_neg:
            ## CASE found lowest fuel usage! Exit while loop
            lowest_fuel = fuel
            horizontal_pos = guess
            stop = 1
        else:
            ## CASE neg incr uses less fuel than current guess
            ##  head that direction
            guess -= 1
    else:
        ## CASE pos incr uses less fuel than current guess
        ##  head that direction
        guess += 1
            
print(f'Answer: {lowest_fuel}')



## Stats  ######################################################

## Track when started and when complete
## Update track_time_num to match num so this prints correctly
## Only update track_time_num if tracked time of task completions
track_time_num = 7
if track_time_num == num:
    start_time = datetime.datetime(2021,12,num,12,44)
    finish_part1 = datetime.datetime(2021,12,num,13,20)
    finish_part2 = datetime.datetime(2021,12,num,13,34)

    print(f'\n\nStats ######################################################')
    print(f'For Day {num}: ')
    print(f'Rhiannon completed Task 1     in {finish_part1 - start_time}')
    print(f'Rhiannon completed Task 1 & 2 in {finish_part2 - start_time}')


