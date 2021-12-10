import pandas as pd
import numpy as np
import datetime


import advent_of_code as aoc

## Read in input
num = 9
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = False


## Functions ##################################################

def get_nearby_indices(df,basin):
    '''basin = list of [x,y] indices, which are indices of df (x = row, y = col). 
       Function check for nearby indices
       Returns list of indices (example [[x1,y1],[x2,y2] ...])
    '''
    xmax,ymax = df.shape 
    nearby = []
    
    for x, y in basin:
        if (x > 0) and (x < xmax - 1) and (y > 0) and (y < ymax -1):
            nearby.extend([[x+1,y],
                           [x-1,y],
                           [x,y-1],
                           [x,y+1],])

        elif (x == 0):
            if (y == 0):
                nearby.extend([[x+1,y],
                               [x,y+1]]
                              )
            elif (y < ymax - 1):
                nearby.extend([[x,y-1],
                               [x,y+1],
                               [x+1,y]])

            else:
                ## CASE y == ymax - 1
                nearby.extend([[x+1,y],
                               [x,y-1]])

        elif (x == xmax - 1):
            if (y == 0):
                nearby.extend([[x,y+1],
                               [x-1,y]])
            elif (y < ymax - 1):
                nearby.extend([[x,y-1],
                               [x,y+1],
                               [x-1,y]])
            else:
                ## CASE y == ymax - 1
                nearby.extend([[x,y-1],
                               [x-1,y]])


        elif (y == 0):
            if (x < xmax - 1):
                nearby.extend([[x-1,y],
                               [x+1,y],
                               [x,y+1]])

        elif (y == ymax - 1):
            if (x < xmax - 1):
                nearby.extend([[x-1,y],
                               [x+1,y],
                               [x,y-1]])

    return nearby

    
def check_x_y_low(df,x,y):
    '''x,y are indices of df, specifying a position: df.loc[x,y]
       Returns list of indices (example [[x1,y1],[x2,y2] ...])
    '''

    xmax,ymax = df.shape 
    check = []
    if (x > 0) and (x < xmax - 1) and (y > 0) and (y < ymax -1):
        check.append(df.loc[x-1,y])
        check.append(df.loc[x+1,y])
        check.append(df.loc[x,y-1])
        check.append(df.loc[x,y+1])
        return check
    
    elif (x == 0):
        if (y == 0):
            check.append(df.loc[x,y+1])
            check.append(df.loc[x+1,y])
        elif (y < ymax - 1):
            check.append(df.loc[x,y-1])
            check.append(df.loc[x,y+1])
            check.append(df.loc[x+1,y])
        else:
            ## CASE y == ymax -1
            check.append(df.loc[x,y-1])
            check.append(df.loc[x+1,y])

        return check
            
    elif (x == xmax - 1):
        if (y == 0):
            check.append(df.loc[x,y+1])
            check.append(df.loc[x-1,y])
        elif (y < ymax - 1):
            check.append(df.loc[x,y-1])
            check.append(df.loc[x,y+1])
            check.append(df.loc[x-1,y])
        else:
            ## CASE y == ymax - 1
            check.append(df.loc[x,y-1])
            check.append(df.loc[x-1,y])

        return check
    elif (y == 0):
        if (x < xmax - 1):
            check.append(df.loc[x-1,y])
            check.append(df.loc[x+1,y])
            check.append(df.loc[x,y+1])
            
        return check
    elif (y == ymax - 1):
        if (x < xmax - 1):
            check.append(df.loc[x-1,y])
            check.append(df.loc[x+1,y])
            check.append(df.loc[x,y-1])

        return check

## PART 1  ##################################################
## Format input as df grid.
to_df = []
for line in lines:
    iline = [int(i) for i in line]
    to_df.append(iline)

df = pd.DataFrame(to_df)

## Check for local minima, iterating through x (rows) and y (columns)
summm = 0
for x in df.index:
    for y in df.columns:
        if all(df.loc[x,y] < check_x_y_low(df,x,y)):
            summm = summm + 1 + df.loc[x,y]

print(f'Answer: {summm}')



## PART 2  ##################################################

to_df = []
for line in lines:
    iline = [int(i) for i in line]
    to_df.append(iline)

df = pd.DataFrame(to_df)

## Initial check. Find all local minima
## basins is a list of [x,y] of local minima
basins = []
for x in df.index:
    for y in df.columns:
        if all(df.loc[x,y] < check_x_y_low(df,x,y)):
            basins.append([[x,y]])

## Expand size of each basin until reach outer edge, outer edge == 9
## big_basin is list of positions making up the larger basins.
big_basins = []
for basin in basins:
    stop_basin = 0
    
    while stop_basin == 0:
        ## Get positions of points near all points in basin
        ind_to_check = get_nearby_indices(df,basin)
        ind_to_check2 = ind_to_check.copy()

        ## For each position:
        ##  do not need if position already in basin
        ##  do not need if outer edge (==9)
        ## Positions left are added to the basin and are next up to check in while loop
        for ind in ind_to_check:
            if ind in basin:
                ind_to_check2.remove(ind)
            if df.loc[ind[0],ind[1]] == 9:
                ind_to_check2.remove(ind)
                
        if verbose:
            print(ind_to_check)
            print(ind_to_check2)

        ## If positions left, add to basin and list to check in next while loop iteration
        if len(ind_to_check2):
            ind_to_check = []
            for ind in ind_to_check2:
                if ind not in basin:
                    basin.append(ind)
                    ind_to_check.append(ind)
            if verbose:
                print(basin)
                print(ind_to_check)
        else:
            ## CASE no positions in ind_to_check2, nothing left to check or add to basin
            ## Save basin to list of big_basins
            big_basins.append(basin)
            stop_basin = 1

## Get size of 3 largest basins
len_big_basin = [len(i) for i in big_basins]
len_big_basin.sort()
product = len_big_basin[-3] * len_big_basin[-2] * len_big_basin[-1]   
    

print(f'Answer: {product}')    
        

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

