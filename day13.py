import pandas as pd
import numpy as np
import datetime


import advent_of_code as aoc

## Read in input
num = 13
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = False


## Functions ##################################################
def fold_horiz(df,foldstr):
    #foldstr = 'y=7'
    foldind = int(foldstr)
    ## check if yy is a 'y'
    
    topdf = df.loc[:foldind-1,:].copy()
    bottomdf = df.loc[foldind+1:,:].copy()
    bottomdf = bottomdf.iloc[::-1].reset_index(drop=True) 

    return topdf + bottomdf

def fold_vert(df,foldstr):
    #foldstr = 'x=5'
    foldind = int(foldstr)
    ## check if yy is a 'y'
    
    leftdf = df.iloc[:,:foldind].copy()
    rightdf = df.iloc[:,foldind+1:].copy()

    leftcols = leftdf.shape[1]
    rightcols = rightdf.shape[1]

    if leftcols > rightcols:
        cols_to_add = leftcols - rightcols
        rightdf = pd.concat([rightdf,pd.DataFrame(0,index=rightdf.index,columns=range(cols_to_add))],axis=1)
    rightdf = rightdf[rightdf.columns[::-1]]
    rightdf.columns = range(foldind)

    return leftdf + rightdf


## PART 1  ##################################################

dots = [line for line in lines if (line != '') and ('fold' not in line)] 
folds = [line for line in lines if 'fold' in line]

to_df = []
ymax = 0
xmax = 0
for dot in dots:
    dotx,doty = dot.split(',')
    doty = int(doty)
    dotx = int(dotx)
    if doty > ymax:
        ymax = doty
    if dotx > xmax:
        xmax = dotx
    to_df.append([doty,dotx])

df = pd.DataFrame(0,index=range(ymax+1),columns=range(xmax+1))

for point in to_df:
    df.loc[point[0],point[1]] = 1

for fold in folds[:1]:
    ifold = fold.split(' ')[-1]

    x_or_y,foldind = ifold.split('=')

    if x_or_y == 'y':
        df = fold_horiz(df,foldind)
    else:
        df = fold_vert(df,foldind)

summ = sum(df.astype(bool).sum(axis=0))

print(f'Answer: {summ}')

## PART 2  ##################################################

dots = [line for line in lines if (line != '') and ('fold' not in line)] 
folds = [line for line in lines if 'fold' in line]

to_df = []
ymax = 0
xmax = 0
for dot in dots:
    dotx,doty = dot.split(',')
    doty = int(doty)
    dotx = int(dotx)
    if doty > ymax:
        ymax = doty
    if dotx > xmax:
        xmax = dotx
    to_df.append([doty,dotx])

df = pd.DataFrame(0,index=range(ymax+1),columns=range(xmax+1))

for point in to_df:
    df.loc[point[0],point[1]] = 1

for fold in folds:
    ifold = fold.split(' ')[-1]

    x_or_y,foldind = ifold.split('=')

    if x_or_y == 'y':
        df = fold_horiz(df,foldind)
    else:
        df = fold_vert(df,foldind)

## Read output from df 
newdf = df.copy()
newdf[newdf == 0] = '.'
print(newdf)

#print(f'Answer: {summ}')
        

## Stats  ######################################################

## Track when started and when complete
## Update track_time_num to match num so this prints correctly
## Only update track_time_num if tracked time of task completions
track_time_num = 13
if track_time_num == num:
    start_time = datetime.datetime(2021,12,num,18,8)
    finish_part1 = datetime.datetime(2021,12,num,19,4)
    finish_part2 = datetime.datetime(2021,12,num,19,11)

    print(f'\n\nStats ######################################################')
    print(f'For Day {num}: ')
    print(f'Rhiannon completed Task 1     in {finish_part1 - start_time}')
    print(f'Rhiannon completed Task 1 & 2 in {finish_part2 - start_time}')

