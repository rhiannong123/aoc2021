import pandas as pd
import numpy as np
import datetime
import re

import advent_of_code as aoc

## Read in input
num = 16
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = False


## Functions ##################################################
def parse_header(ibin):
    header = {}

    vers = int(ibin[:3],2)
    ibin = ibin[3:]
    typeid = int(ibin[:3],2)
    ibin = ibin[3:]

    header['version'] = vers
    header['typeid'] = typeid

    return header,ibin

def parse_operator_header(ibin):

    operator = {}
    
    operator['length_type_id'] = int(ibin[0])
    ibin = ibin[1:]

    if operator['length_type_id'] == 0:
        operator['bit_length'] = int(ibin[:15],2)
        ibin = ibin[15:]
        operator['num_sub_packets'] = -1
        op_length = 16
    else:
        operator['num_sub_packets'] = int(ibin[:11],2)
        ibin = ibin[11:]
        operator['bit_length'] = -1
        op_length = 12
        
    return operator, op_length, ibin

def parse_literal(ibin):

    literal_length = 0
    number = ''
    while True:
        if ibin[0] == '1':
            ibin = ibin[1:]
            number += ibin[:4]
            literal_length += 5
            ibin = ibin[4:]
        else:
            ibin = ibin[1:]
            number += ibin[:4]
            ibin = ibin[4:]
            literal_length += 5
            break
    literal = int(number,2)

    return literal, literal_length, ibin

def remove_trailing_zeros(ibin):
    ibin 

## PART 1  ##################################################

# Input is a line of hex. Get expected hex length to keep leading zeros
line = lines[0]
hsize = len(line) * 4

# Convert hex to integer
ibin = (bin(int(line, 16))[2:]).zfill(hsize)

version_count = 0
packets_to_parse = 1
sub_length = []
while True:

    # Parse header, increment version count
    header, ibin = parse_header(ibin)
    version_count += header['version']
    if verbose:
        print(header)
    
    if header['typeid'] == 4:
        # Current packet is a literal, get number and bit_length
        literal, lit_length, ibin = parse_literal(ibin)
        if verbose:
            print(sub_length,literal)
        
        # If in a packet that is keeping track of packet length, decrement sub_length
        if sub_length != []:
            for idx in range(len(sub_length)):
                # Take into account header length (the 6)
                sub_length[idx] = sub_length[idx] - lit_length - 6
            if sub_length[-1] == 0:
                sub_length.pop(-1)
            if sub_length != []:
                packets_to_parse += 1
                
        if verbose:
            print('sub_length', sub_length)

    else:
        ## CASE packet is not literal, typeid != 4
        operator,op_length,ibin = parse_operator_header(ibin)
        if verbose:
            print(operator)

        # If in a packet that is keeping track of packet length, decrement sub_length
        if sub_length != []:
            for idx in range(len(sub_length)):
                sub_length[idx] = sub_length[idx] - op_length - 6
            if sub_length[-1] == 0:
                sub_length.pop(-1)
        
        if operator['length_type_id'] == 1:
            packets_to_parse += operator['num_sub_packets']
            
        else:
            sub_length.append(operator['bit_length'])
            packets_to_parse += 1
            
    packets_to_parse -= 1
    print('packets left: ', packets_to_parse)
    
    if (packets_to_parse == 0) or (all(True if char == '0' else False for char in ibin)) or (ibin == ''):
        break
            
            
print(f'Answer: {version_count}')
## packets_to_parse counter is not decrementing correctly, but I get the version count so yay?






## PART 2  ##################################################
template = lines[0]

clean_dict = {}
pair_dict = {}
for line in lines[2:]:
    k,v = line.split(' -> ')
    pair_dict[k] = f'{k[0]}:{v};{k[1]}'
    clean_dict[k] = f'{k[0]}{v}{k[1]}'

poly = template
steps = 8
start = datetime.datetime.now()
for step in range(steps):

    ## Can get count of these later..., testing for speed
    poly = poly.replace('NB','B')

    for pair in pair_dict:
        poly = re.sub(pair,pair_dict[pair],poly)
        poly = re.sub(pair,pair_dict[pair],poly)
    poly = re.sub(':','',poly)
    poly = re.sub(';','',poly)
    #print(step, '   ',poly)
    print(step)
    print(datetime.datetime.now() - start)



    
'''
poly = template
steps = 40
for step in range(steps):
    for pair in pair_dict:
        poly = re.sub(pair,pair_dict[pair],poly)
        poly = re.sub(pair,pair_dict[pair],poly)
    poly = re.sub(':','',poly)
    poly = re.sub(';','',poly)
    print(step)
    print(datetime.datetime.now())
'''


'''    
poly = template
steps = 10
for step in range(steps):
    pairs = [poly[i]+poly[i+1] for i in range(len(poly)-1)]
    lspairs = list(set(pairs))
    pairs = list(set(pairs))
    for pair in pairs:
        if pair in pair_dict:
            poly = poly.replace(pair,pair_dict[pair])
            poly = poly.replace(pair,pair_dict[pair])            
    poly = poly.replace(':','').replace(';','')
    print(step)
'''    
letters = list(set(list(poly)))
most = ''
most_count = 0
least = letters[0]
least_count = len(poly)
for letter in letters:
    letter_count = sum([1 for i in poly if i == letter])
    if most_count < letter_count:
        most = letter
        most_count = letter_count
    if least_count > letter_count:
        least = letter
        least_count = letter_count

print(f'Answer: {most_count-least_count}')





    
poly = template
steps = 10
for step in range(steps):
    pairs = [poly[i]+poly[i+1] for i in range(len(poly)-1)]
    first_ind = [i for i in range(len(poly)-1)]
    ind_to_add = 0
    for fi,pair in zip(first_ind,pairs):
        if pair in pair_dict:
            ind = ind_to_add + fi
            poly = poly[:ind+1] + pair_dict[pair] + poly[ind+1:]
            ind_to_add += 1
    print(step)
    
letters = list(set(list(poly)))
most = ''
most_count = 0
least = letters[0]
least_count = len(poly)
for letter in letters:
    letter_count = sum([1 for i in poly if i == letter])
    if most_count < letter_count:
        most = letter
        most_count = letter_count
    if least_count > letter_count:
        least = letter
        least_count = letter_count

print(f'Answer: {most_count-least_count}')



## Stats  ######################################################

## Track when started and when complete
## Update track_time_num to match num so this prints correctly
## Only update track_time_num if tracked time of task completions
track_time_num = 13
if track_time_num == num:
    start_time = datetime.datetime(2021,12,num,18,11)
    finish_part1 = datetime.datetime(2021,12,num,18,42)
    finish_part2 = datetime.datetime(2021,12,num,19,11)

    print(f'\n\nStats ######################################################')
    print(f'For Day {num}: ')
    print(f'Rhiannon completed Task 1     in {finish_part1 - start_time}')
    print(f'Rhiannon completed Task 1 & 2 in {finish_part2 - start_time}')

