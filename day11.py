import pandas as pd
import numpy as np
import datetime


import advent_of_code as aoc

## Read in input
num = 11
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = False


## Functions ##################################################

def get_nearby_indices(df,x,y):
    '''Function to return nearby indices given df.loc[x,y]
       If close to the edge, remove from nearby indices
    '''
    nearby = [[x-1,y-1],
              [x+0,y-1],
              [x+1,y-1],
              [x-1,y+0],
              [x+1,y+0],
              [x-1,y+1],
              [x+0,y+1],
              [x+1,y+1],
              ]

    if x-1 < 0:
        nearby.remove([x-1,y-1])
        nearby.remove([x-1,y])
        nearby.remove([x-1,y+1])
    elif x+1 == df.shape[0]:
        nearby.remove([x+1,y-1])
        nearby.remove([x+1,y])
        nearby.remove([x+1,y+1])

    if y-1 < 0:
        if [x-1,y-1] in nearby:
            nearby.remove([x-1,y-1])
        if [x+1,y-1] in nearby:
            nearby.remove([x+1,y-1])

        nearby.remove([x+0,y-1])
    elif y+1 == df.shape[1]:
        if [x-1,y+1] in nearby:
            nearby.remove([x-1,y+1])
        if [x+1,y+1] in nearby:
            nearby.remove([x+1,y+1])

        nearby.remove([x+0,y+1])

    return nearby

## PART 1  ##################################################
## Format input as df grid.            
to_df = []
for line in lines:
    iline = [int(i) for i in line]
    to_df.append(iline)

df = pd.DataFrame(to_df)

## Iterate over 100 steps
steps = 100
flash_count = 0
for step in range(steps):
    print(step)

    ## Increment each octopus 1 energy level
    df = df + 1

    ## as octopuses flash, loop over new ones that flashed (==10)
    stop = 0
    while stop == 0:
        ## reset ten_found this round, only set to 1 if a new flash occurred
        ten_found = 0

        ## Find new flashes, if any
        for x in df.index: 
            for y in df.columns:
                ## For any new flash found,
                ##  set df[x,y] to not 10
                ##  increment flash count
                ##  increment nearby neighbors, if any == 10, iterate through while loop again
                if df.loc[x,y] == 10:
                    df.loc[x,y] = 11 # will reset before next step
                    flash_count += 1
                    nearbys = get_nearby_indices(df,x,y)
                    for inearby in nearbys:
                        nx = inearby[0] 
                        ny = inearby[1] 
                        if df.loc[nx,ny] != 10:
                            df.loc[nx,ny] = df.loc[nx,ny] + 1
                        if df.loc[nx,ny] == 10:
                            ten_found = 1
                        ten_found = 1

        ## CASE no new 10s found this round, exit while loop, set any >10 back to 0
        if ten_found == 0:
            for x in df.index: 
                for y in df.columns:
                    if df.loc[x,y] >= 10:
                        df.loc[x,y] = 0
            stop = 1

print(f'Answer: {flash_count}')

## PART 2  ##################################################

to_df = []
for line in lines:
    iline = [int(i) for i in line]
    to_df.append(iline)

df = pd.DataFrame(to_df)

steps = 500
flash_count = 0
synchro_found = 0
for step in range(1,steps+1):

    print(step)

    ## Check if synchronized flash already happened, if so skip ahead, we are done
    if synchro_found == 1:
        continue
    
    ## Increment each octopus 1 energy level
    df = df + 1

    ## as octopuses flash, loop over new ones that flashed (==10)
    stop = 0
    while stop == 0:
        ## reset ten_found this round, only set to 1 if a new flash occurred
        ten_found = 0

        ## Find new flashes, if any
        for x in df.index: 
            for y in df.columns:
                ## For any new flash found,
                ##  set df[x,y] to not 10
                ##  increment flash count
                ##  increment nearby neighbors, if any == 10, iterate through while loop again
                if df.loc[x,y] == 10:
                    df.loc[x,y] = 11 # will reset before next step
                    flash_count += 1
                    nearbys = get_nearby_indices(df,x,y)
                    for inearby in nearbys:
                        nx = inearby[0] 
                        ny = inearby[1] 
                        if df.loc[nx,ny] != 10:
                            df.loc[nx,ny] = df.loc[nx,ny] + 1
                        if df.loc[nx,ny] == 10:
                            ten_found = 1
                        ten_found = 1

        ## CASE no new 10s found this round, exit while loop, set any >10 back to 0
        if ten_found == 0:
            for x in df.index: 
                for y in df.columns:
                    if df.loc[x,y] >= 10:
                        df.loc[x,y] = 0
            stop = 1

        ## Check if all dataframe is now 10 or greater
        ## Increment synchro_count for each positioin greater than 10
        synchro_count = 0
        for x in df.index:
            for y in df.columns:
                if df.loc[x,y] > 9:
                    synchro_count += 1

        ## If synchro_count equal to the size of dataframe, we are done
        if synchro_count == df.shape[0]*df.shape[1]:
            print(f'!!!!! STEP {step}', df)
            synchro_found = 1

        ## Exit while loop, set all 10s or greater = 0
        if ten_found == 0:
            for x in df.index: 
                for y in df.columns:
                    if df.loc[x,y] >= 10:
                        df.loc[x,y] = 0
            stop = 1

        

## Stats  ######################################################

## Track when started and when complete
## Update track_time_num to match num so this prints correctly
## Only update track_time_num if tracked time of task completions
track_time_num = 9
if track_time_num == num:
    start_time = datetime.datetime(2021,12,num,17,34)
    finish_part1 = datetime.datetime(2021,12,num,18,15)
    finish_part2 = datetime.datetime(2021,12,num,19,13)

    print(f'\n\nStats ######################################################')
    print(f'For Day {num}: ')
    print(f'Rhiannon completed Task 1     in {finish_part1 - start_time}')
    print(f'Rhiannon completed Task 1 & 2 in {finish_part2 - start_time}')

