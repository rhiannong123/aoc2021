import pandas as pd
import numpy as np
import datetime


import advent_of_code as aoc

## Read in input
num = 12
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = False


## Functions ##################################################

## PART 1  ##################################################
## Each line is a point to point direction (caves) on a map
## Create dict of what caves are directly connected
## key: one cave
## value: list of all cave(s) that the dict.key is connected
caves = {}

for line in lines: 
    ## cave 1 to cave 2
    path0,path1 = line.split('-')

    ## if cave 1 not defined in caves yet, add it to dict
    if path0 not in caves: 
        caves[path0] = [path1] 
    else: 
        if path1 not in caves[path0]: 
            caves[path0].append(path1)

    ## Define in caves the other way, not just 1 to 2, but 2 to 1
    if path1 not in caves: 
        caves[path1] = [path0] 
    else: 
        if path0 not in caves[path1]: 
            caves[path1].append(path0)  
        
## Initialize paths
paths = [f'start,{i}' for i in caves['start']]

stop = 0
while stop == 0:
    new_paths = []
    for path in paths:
        print(f'working on {path}')
        
        ## add to end of path. discard path if it means entering a small cave twice
        caves_in_path = path.split(',')
        last_cave_in_path = caves_in_path[-1]
        if (last_cave_in_path == 'bad') or (last_cave_in_path == 'end'):
            new_paths.append(path)
            continue
        
        for cave in caves[last_cave_in_path]:
            if cave == 'start':
                continue
            if cave.lower() in path.split(','):
                ## small cave already in path, path bad
                new_path = f'{path},{cave},bad'
                new_paths.append(new_path)
                continue

            new_path = f'{path},{cave}'
            new_paths.append(new_path)

    paths = new_paths.copy()

    end_bad_paths = [path for path in paths if (path.split(',')[-1] == 'end') or (path.split(',')[-1] == 'bad')]
    if len(paths) == len(end_bad_paths):
        stop = 1
    
    ## End while loop if each path ends with 'end'


num_paths = sum([1 for path in paths if path.split(',')[-1] == 'end']) 
print(f'Answer: {num_paths}')

## PART 2  ##################################################
## Each line is a point to point direction (caves) on a map
## Create dict of what caves are directly connected
## key: one cave
## value: list of all cave(s) that the dict.key is connected
caves = {}

for line in lines: 
    ## cave 1 to cave 2
    path0,path1 = line.split('-')

    ## if cave 1 not defined in caves yet, add it to dict
    if path0 not in caves: 
        caves[path0] = [path1] 
    else: 
        if path1 not in caves[path0]: 
            caves[path0].append(path1)

    ## Define in caves the other way, not just 1 to 2, but 2 to 1
    if path1 not in caves: 
        caves[path1] = [path0] 
    else: 
        if path0 not in caves[path1]: 
            caves[path1].append(path0)  
                
## initialize paths
## cave_twice list of flags length of paths list
##   cave_twice is -1 for bad or end paths, 1 if a small cave has been entered a second time,
##   
paths = [f'start,{i}' for i in caves['start']]
cave_twice = [0 for i in caves['start']]

stop = 0
while stop == 0:
    
    new_paths = []
    new_cave_twice = []
    
    for icave_twice,path in zip(cave_twice,paths):
        if verbose:
            print(len(paths))

        ## Add to end of path.
        ## One small cave can be entered in twice, any other paths label as bad
        caves_in_path = path.split(',')
        last_cave_in_path = caves_in_path[-1]
        if (last_cave_in_path == 'bad') or (last_cave_in_path == 'end'):
            new_paths.append(path)
            new_cave_twice.append(-1)
            continue
        
        for cave in caves[last_cave_in_path]:
            if cave == 'start':
                continue

            ## CASE small cave found, check if valid
            if (cave.lower() in path.split(',')):

                if icave_twice == 1:
                    ## one small cave visited twice already, now it's a bad path
                    new_path = f'{path},{cave},bad'
                    new_paths.append(new_path)
                    new_cave_twice.append(-1)
                    continue
                else:
                    ## CASE first small cave to be visited twice,
                    ## cave twice flag = 1 for this cave
                    new_path = f'{path},{cave}'
                    new_paths.append(new_path)
                    new_cave_twice.append(1)
                    continue

            ## CASE cave is a large cave, path valid, keep same cave twice flag
            new_path = f'{path},{cave}'
            new_paths.append(new_path)
            if icave_twice:
                new_cave_twice.append(1)
            else:
                new_cave_twice.append(0)
            
    paths = new_paths.copy()
    cave_twice = new_cave_twice.copy()

    ## End while loop if each path ends with 'end' or 'bad'
    end_bad_paths = [path for path in paths if (path.split(',')[-1] == 'end') or (path.split(',')[-1] == 'bad')]
    if len(paths) == len(end_bad_paths):
        stop = 1
    


num_paths = sum([1 for path in paths if path.split(',')[-1] == 'end']) 
print(f'Answer: {num_paths}')

        

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

