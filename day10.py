import pandas as pd
import numpy as np
import datetime


import advent_of_code as aoc

## Read in input
num = 10
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = False


## Functions ##################################################


## PART 1  ##################################################

syntax_scoring = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
    }

closing_dict = {'>':'<', '}':'{', ']':'[', ')':'('}
opening_dict = {'<':'>', '{':'}', '[':']', '(':')'}

syntax_sum = 0
for line in lines:

    ## Keep track of indices of line that have been checked (checked_ind)
    ## An unchecked open character value = 0
    ## A checked open character, closed character pair checked_ind values will be their index in line 
    stop = 0
    bad_char = ''
    checked_ind = [-1]*len(line)
    for chidx,char in enumerate(line):

        if stop == 1:
            continue

        if verbose:
            print(checked_ind)

        ## Keep track of unchecked open characters by updating value of checked_ind = 0
        if char in opening_dict:
            checked_ind[chidx] = 0
            continue
        
        if char in closing_dict:
            expected = closing_dict[char]

            ## Update checked_ind with index of closing char
            ## Compare to latest unchecked open char (indicated where checked_ind = 0)
            checked_ind[chidx] = chidx
            unchecked_open_idx = max([i for i in range(len(checked_ind)) if checked_ind[i] == 0]) 
            if line[unchecked_open_idx] == expected:
                ## CASE valid closing character found, update checked_ind of corresponding open char
                checked_ind[unchecked_open_idx] = unchecked_open_idx
            else:
                ## CASE stop work on this line, bad character found
                stop = 1
                bad_char = char
                if verbose:
                    print(f'broken here: expected "{expected}", got "{line[unchecked_open_idx]}"...',line[:unchecked_open_idx])

    ## Bad character found in current line, update syntax sum
    if stop == 1:
        syntax_sum += syntax_scoring[bad_char]

print(f'Answer: {syntax_sum}')




## PART 2  ##################################################

syntax_scoring = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
    }

autocomplete = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
    }

closing_dict = {'>':'<', '}':'{', ']':'[', ')':'('}
opening_dict = {'<':'>', '{':'}', '[':']', '(':')'}

total_score = []
for line in lines:

    ## Keep track of indices of line that have been checked (checked_ind)
    ## An unchecked open character value = 0
    ## A checked open character, closed character pair checked_ind values will be their index in line 
    stop = 0
    checked_ind = [-1]*len(line) 
    for chidx,char in enumerate(line):

        if stop == 1:
            continue

        if verbose:
            print(checked_ind)
            
        ## Keep track of unchecked open characters by updating value of checked_ind = 0
        if char in opening_dict:
            checked_ind[chidx] = 0
            continue
        
        if char in closing_dict:
            expected = closing_dict[char]

            ## Update checked_ind with index of closing char
            ## Compare to latest unchecked open char (indicated where checked_ind = 0)
            checked_ind[chidx] = chidx
            unchecked_open_idx = max([i for i in range(len(checked_ind)) if checked_ind[i] == 0]) 
            if line[unchecked_open_idx] == expected:
                ## CASE valid closing character found, update checked_ind of corresponding open char
                checked_ind[unchecked_open_idx] = unchecked_open_idx
            else:
                ## CASE stop work on this line, bad character found
                stop = 1
                if verbose:
                    print(f'broken here: expected "{expected}", got "{line[unchecked_open_idx]}"...',line[:unchecked_open_idx])

    ## If line found to be good (i.e. no bad char found), stop = 0
    ## score based on closing characters needed to complete line
    score = 0
    if stop == 0:
        ## Line was not corrupt
        ## Get open indices, reverse the order, get corresponding closing characters
        unresolved_open_indices = [i for i in range(len(checked_ind)) if checked_ind[i] == 0]
        unresolved_open_indices.reverse()
        for ind in unresolved_open_indices:
            closed_needed = opening_dict[line[ind]]
            score = score * 5 + autocomplete[closed_needed] 

    ## if score != 0, i.e. line was not corrupt, just incomplete, add to total_score list
    if score != 0:
        total_score.append(score)

## sort total score before calculating median
total_score.sort()
    
        
print(f'Answer: {int(np.median(total_score))}')





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

