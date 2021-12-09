import pandas as pd
import numpy as np
import datetime


import advent_of_code as aoc

## Read in input
num = 8
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = False


## Functions ##################################################

def check_output_for_unique(output, digits):
    
    for digit in UNIQUE_DIGITS:
        checks = [i for i in output if len(i) == digits[digit]['segment_count']]
        if checks != []:
            for check in checks:
                if 'signals' in digits[digit]:
                    digits[digit]['signals'].append(check)
                else:
                    digits[digit]['signals'] = [check]
                    

            if verbose:
                print(f'Updated: {digit} signals: ', digits[digit]['signals'])
    return digits
        



## PART 1  ##################################################
## FWIW I started coding this one way because I did NOT understand the input or where part 2 might go
DIGITS = {
    'one': {'segment_count': 2
            },
    'four': {'segment_count': 4
             },
    'seven': {'segment_count': 3
              },
    'eight': {'segment_count': 7
              },
}

UNIQUE_DIGITS = ['one','four','seven','eight']

## Only need RHS of pipe for this part
outputs = [line.split('|')[1] for line in lines]
digits = DIGITS.copy()


for output in outputs:
    ## Clean up output
    output = output.strip().split(" ")

    ## Function will check for unique digit, and append to list in dictionary
    digits = check_output_for_unique(output, digits)

summm = 0
for digit in UNIQUE_DIGITS:
    if 'signals' in digits[digit]:
        summm = summm + len(digits[digit]['signals'])
    

print(f'Answer: {summm}')



## PART 2  ##################################################
## Each line is {input} | {output}
inputs = [line.split('|')[0] for line in lines]
outputs = [line.split('|')[1] for line in lines]

total_sum = 0
for iinput,ioutput in zip(inputs,outputs):

    ## Clean up iinput, ioutput
    iinput = iinput.strip().split(' ') 
    ioutput = ioutput.strip().split(' ')

    ## Define a digits dictionary
    ## digits.key is str(int) for int 0 thru 9
    ## digits.value is the set of letters associated with that number
    digits = {}

    ## Can define 1, 4, 7, 8 right away based on length of letters that make up the number signal
    digits['1'] = set([i for i in iinput if len(i) == 2][0])
    digits['4'] = set([i for i in iinput if len(i) == 4][0])
    digits['7'] = set([i for i in iinput if len(i) == 3][0])
    digits['8'] = set([i for i in iinput if len(i) == 7][0])

    
    ## For number signals that are 6 letters long, options are 0, 6 and 9
    ## 9 is the sixlong digit that has all of 4's letters
    ## 0 is the sixlong digit that has all of 7's letters
    ## 6 is the sixlong digit that is left
    
    sixlong = [i for i in iinput if len(i) == 6]

    nine = [sixdigit for sixdigit in sixlong if digits['4'].issubset(sixdigit)][0]
    digits['9'] = set(nine)
    sixlong.remove(nine)
    
    zero = [sixdigit for sixdigit in sixlong if digits['7'].issubset(sixdigit)][0]
    digits['0'] = set(zero)
    sixlong.remove(zero)

    six = sixlong[0]
    digits['6'] = set(sixlong[0])


    ## For number signals that are 5 letters long, options are 2, 3, and 5
    ## 3 is the fivelong digit that has all of 1's letters
    ## 2 and 5 are left, but all of 5's letters will be in 6
    fivelong = [i for i in iinput if len(i) == 5]

    three = [fivedigit for fivedigit in fivelong if digits['1'].issubset(fivedigit)][0]
    digits['3'] = set(three)
    fivelong.remove(three)

    if set(fivelong[0]).issubset(digits['6']):
        digits['5'] = set(fivelong[0])
        digits['2'] = set(fivelong[1])
    else:
        digits['5'] = set(fivelong[1])
        digits['2'] = set(fivelong[0])

    ## Use digits dictionary and decode each output
    decoded = []
    for output in ioutput:
        for digit,iset in digits.items():
            if verbose:
                print(digit,iset)
            ## Check if letters in output are the same as letters as current digit
            ## If so save to decoded
            if set(output) == iset:
                if verbose:
                    print('found it!   ',digit,output)
                decoded.append(digit)

    ## Turn decoded into a string, then integer, add to sum
    total_sum = total_sum + int(''.join(decoded))


print(f'Answer: {total_sum}')
    
        

## Stats  ######################################################

## Track when started and when complete
## Update track_time_num to match num so this prints correctly
## Only update track_time_num if tracked time of task completions
track_time_num = 8
if track_time_num == num:
    start_time = datetime.datetime(2021,12,num,15,30)
    finish_part1 = datetime.datetime(2021,12,num,16,25)
    finish_part2 = datetime.datetime(2021,12,num,22,38)

    print(f'\n\nStats ######################################################')
    print(f'For Day {num}: ')
    print(f'Rhiannon completed Task 1     in {finish_part1 - start_time}')
    print(f'Rhiannon completed Task 1 & 2 in {finish_part2 - start_time}')

