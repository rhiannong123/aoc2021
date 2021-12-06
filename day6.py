import pandas as pd
import numpy as np
import datetime


import advent_of_code as aoc

## Read in input
num = 6
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = True




## Functions ##################################################
def incr_one_day(state):
    ''' state is a numpy array
    '''

    state = state - 1
    find_neg_ones = np.where(state == -1)[0]

    ## WHY DOESN'T np array have an extend in place??
    if find_neg_ones.size > 0:
        state_list = state.tolist()
        state_list.extend(find_neg_ones.size*[8])
        state = np.array(state_list)
    state[find_neg_ones] = 6

    return state    

## PART 1  ##################################################
init = [int(fish) for fish in lines[0].split(',')]
state = np.array(init)

#ndays = 18
ndays = 80
for iday in range(ndays):
    state = incr_one_day(state)
    if verbose:
        print(state)

print(f'Answer: {state.size}')




## PART 2  ##################################################

## Way of doing PART 1 waaaaay too slow, redid to optimize
init_time = datetime.datetime.now()
init = [int(fish) for fish in lines[0].split(',')]
ndays = 256

## Go through initial set of fish
## Track new fish in nfish_dict
## nfish_dict key = day new fish spawned
## nfish_dict value = number of new fish spawned that day
total_fish = len(init)
nfish_dict = {}
nfish_dict_total = {} ## for troubleshooting only
nitems  = 0 ## for curiousity
for ifish in init:

    if ifish < ndays % 7:
        spawned = int(np.ceil(ndays/7))
    else:
        spawned = int(np.floor(ndays/7))

    for i in range(spawned):
        born_day = i*(7)+ifish+1
        str_born_day = str(born_day)
        if str_born_day in nfish_dict:
            nfish_dict[str_born_day] += 1
            nfish_dict_total[str_born_day] += 1
        else:
            nfish_dict[str_born_day] = 1
            nfish_dict_total[str_born_day] = 1
            nitems += 1
    total_fish += spawned


## Go through each iteration of new fish
## Track new fish in nfish_dict
## nfish_dict key = day new fish spawned
## nfish_dict value = number of new fish spawned that day
## Track newest round of fish in new_nfish_dict (which will be set to nfish_dict at end of while)

stop_while = 0
#counter = 30 ## for troubleshooting while loop
while (stop_while == 0):

    if verbose:
        print(f'Number of iterations in for loop this time: {nitems}')

    ## Go through new batch of spawned fish
    nitems = 0
    new_nfish_dict = {}
    for ifish_key,ifish_val in nfish_dict.items():
        ifish = int(ifish_key)

        ## New fish will spawn 9 days after it spawned
        ## Keep track of fish spawned, handling first spawn differently
        first_spawn_day = ifish + 9
        spawned = []
        if first_spawn_day <= ndays:
            ## CASE: fish will spawn before ndays is over, need to include and track
            spawned.append(first_spawn_day)
            
            ## After initial spawning, a fish will produce a new fish every 7 days
            spawned_after_first = int(np.floor((ndays - first_spawn_day) / 7))
            if spawned_after_first > 0:
                ## CASE: fish will spawn more after first spawn, need to include and track
                spawned.extend([i*(7)+first_spawn_day
                                for i in range(1,spawned_after_first + 1)])

            ## For each new fish, add to new_nfish_dict
            ##  this will become the next dictionary to iterate over (the next nfish_dict)
            for born_day in spawned:
                str_born_day = str(born_day)
                if str_born_day in new_nfish_dict:
                    new_nfish_dict[str_born_day] += ifish_val
                else:
                    new_nfish_dict[str_born_day] = ifish_val
                    nitems += 1

                ## For troubleshooting only
                if str_born_day in nfish_dict_total:
                    nfish_dict_total[str_born_day] += 1
                else:
                    nfish_dict_total[str_born_day] = 1
                    
    ## Track how many fish spawned this time
    total_fish += sum(new_nfish_dict.values())
    if verbose:
        print(f'Total fish: {total_fish}')

    ## If no new fish spawned this time, break while loop
    nfish_dict = new_nfish_dict
    if nfish_dict == {}:
        stop_while = 1

    #counter -= 1
    #if counter == 0:
    #    stop_while = 1
        
stop_time = datetime.datetime.now()
print(f'Answer: {total_fish}')
print(f'Computation time: {stop_time - init_time}')






