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

def check_operator_type(typeid):
    if typeid == 0:
        action = 'sum'
        boolean = False
    elif typeid == 1:
        action = 'product'
        boolean = False
    elif typeid == 2:
        action = 'minimum'
        boolean = False
    elif typeid == 3:
        action = 'maximum'
        boolean = False
    elif typeid == 5:
        action = 'greater than'
        boolean = True
    elif typeid == 6:
        action = 'less than'
        boolean = True
    elif typeid == 7:
        action = 'equal to'
        boolean = True

    return action, boolean


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

# Input is a line of hex. Get expected hex length to keep leading zeros
line = lines[0]
hsize = len(line) * 4

# Convert hex to integer
ibin = (bin(int(line, 16))[2:]).zfill(hsize)

### First build up a dictionary of packets with all the needed info
### Then go through the operators backwards and determine values

### Build up dictionary of packets
opids = []
len_typeids = []
sub_lengths = []
open_statuss = []
num_sub_packets = []
packets = {}
counter = -1

while True:

    literal_packet_closed = 0
    sub_length_packet_closed_this_round = 0
    
    # Parse header
    header, ibin = parse_header(ibin)
    if verbose:
        print('===========================================================================================')
        print(header)
    
    if header['typeid'] == 4:
        # Current packet is a literal, get number and bit_length
        literal, lit_length, ibin = parse_literal(ibin)
        literal_packet_closed = 1

        # Get last opid that is open, add literal to list in opid
        for opid in opids:
            if packets[opid]['open'] == 1:
                opid_literal = opid
        if 'literals' not in packets[opid_literal]:
            packets[opid_literal]['literals'] = []
        packets[opid_literal]['literals'].append(literal)
        packets[opid_literal]['ptype'].append('l')
        
        if verbose:
            print('literal:   ', literal)
        
        # Decrement all active (i.e. not 0 or not -1) sub_lengths
        # If this makes an open packet have sub_length 0, close that packet
        for sidx, sub_length in enumerate(sub_lengths):
            if sub_length == -1:
                continue
            if sub_length != 0:
                sub_lengths[sidx] = sub_lengths[sidx] - lit_length - 6
            if (sub_lengths[sidx] == 0) and (packets[opids[sidx]]['open'] == 1):
                packets[opids[sidx]]['open'] = 0
                open_statuss[sidx] = 0
                sub_length_packet_closed_this_round = +1
                
    else:
        ## CASE packet is not literal, typeid != 4
        operator,op_length,ibin = parse_operator_header(ibin)

        # Initialize operator id variables for packet dict
        counter += 1
        opid = f'op{counter}'
        packets[opid] = {}
        packets[opid]['typeid'] = header['typeid']
        packets[opid]['open'] = 1
        packets[opid]['ptype'] = []

        # Add current opid to list of opids
        opids.append(opid)
        open_statuss.append(1)

        if verbose:
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('operator: ', opid, operator)


        # Decrement all active (i.e. not 0 or not -1) sub_lengths
        # If this makes an open packet have sub_length 0, close that packet
        for sidx, sub_length in enumerate(sub_lengths):
            if sub_length == -1:
                continue
            if sub_length != 0:
                sub_lengths[sidx] = sub_lengths[sidx] - op_length - 6
            if (sub_lengths[sidx] == 0) and (packets[opids[sidx]]['open'] == 1):
                packets[opids[sidx]]['open'] = 0
                open_statuss[sidx] = 0
                sub_length_packet_closed_this_round += 1
                
        # Keep track of operator length type id.
        # Keep track of the two different operator packet categories 
        len_typeids.append(operator['length_type_id'])
        sub_lengths.append(operator['bit_length'])
        if operator['num_sub_packets'] == -1:
            num_sub_packets.append(operator['num_sub_packets'])
        else:
            # Since we are about to decrement number of sub packets, add an additional 1
            num_sub_packets.append(operator['num_sub_packets']+1)

        
        # Add operator to previous operator list
        if len(open_statuss) > 1:
            second_to_last_open_idx = max(idx for idx in range(len(open_statuss[:-1]))
                                          if open_statuss[idx] == 1)
            if 'operators' not in packets[opids[second_to_last_open_idx]]:
                packets[opids[second_to_last_open_idx]]['operators'] = []
                packets[opids[second_to_last_open_idx]]['ptype'] = []
            if opid not in packets[opids[second_to_last_open_idx]]['operators']:
                packets[opids[second_to_last_open_idx]]['operators'].append(opid)
                packets[opids[second_to_last_open_idx]]['ptype'].append('o')


            

    # Decrement last active num_sub_packets
    oidx = len(num_sub_packets) - 1
    num_sub_while = 0
    decrement_this_round = []
    while True:
        if (open_statuss[oidx] == 1) and (num_sub_packets[oidx] > 0) and (oidx not in decrement_this_round):
            num_sub_while = 1
            num_sub_packets[oidx] -= 1
            decrement_this_round.append(oidx)
            if num_sub_packets[oidx] != 0:
                break
            else:
                packets[opids[oidx]]['open'] = 0
                open_statuss[oidx] = 0
                if sum(open_statuss) == 0:
                    break
                oidx = max(idx for idx in range(len(open_statuss)) if open_statuss[idx] == 1)
        else:
            break

    # If sub_length packet closed, check for num_sub decrement
    sub_length_while = 0
    if sub_length_packet_closed_this_round > 0:
        sub_length_while = 1
        oidx = max(idx for idx in range(len(open_statuss)) if open_statuss[idx] == 1)
        while True:
            if sub_length_packet_closed_this_round == -1:
                break
            if (open_statuss[oidx] == 1) and (num_sub_packets[oidx] > 0) and (oidx not in decrement_this_round):
                print(oidx, decrement_this_round)
                num_sub_packets[oidx] -= 1
                decrement_this_round.append(oidx)
                if num_sub_packets[oidx] != 0:
                    break
                else:
                    packets[opids[oidx]]['open'] = 0
                    open_statuss[oidx] = 0
                    if sum(open_statuss) == 0:
                        break
                    oidx = max(idx for idx in range(len(open_statuss)) if open_statuss[idx] == 1)
                    sub_length_packet_closed_this_round -= 1
            else:
                break

    if sum(open_statuss) == 0:
        break    
            
    if (literal_packet_closed == 1):
        oidx = max(idx for idx in range(len(open_statuss)) if open_statuss[idx] == 1)
        while True:
            if (open_statuss[oidx] == 1) and (num_sub_packets[oidx] > 0) and (oidx not in decrement_this_round):
                num_sub_packets[oidx] -= 1
                if num_sub_packets[oidx] != 0:
                    break
                else:
                    packets[opids[oidx]]['open'] = 0
                    open_statuss[oidx] = 0
                    if sum(open_statuss) == 0:
                        break
                    oidx = max(idx for idx in range(len(open_statuss)) if open_statuss[idx] == 1)
            else:
                break
       
            
        
    open_status = [packets[iopid]['open'] for iopid in opids] 
    packets_to_parse = sum(open_status)

    if verbose:
        print(f'sub_lengths:     {sub_lengths}')
        print(f'num_sub_packets: {num_sub_packets}')
        print(f'open_status:     {open_status}')

    if (packets_to_parse == 0) or (all(True if char == '0' else False for char in ibin)) or (ibin == ''):
        break




    

### Go through operator packets backwards and determine values.
opids.reverse()



for opid in opids:

    numbers = []
    
    if 'literals' in packets[opid]:
        lits = packets[opid]['literals'].copy()
    else:
        lits = []
        
    if 'operators' in packets[opid]:
        ops = packets[opid]['operators'].copy()
    else:
        ops = []
        
    for ptype in packets[opid]['ptype']:
        if ptype == 'l':
            numbers.append(lits.pop(0))
        else:
            iop = ops.pop(0)
            numbers.append(packets[iop]['value'])

    new_num = []
    for inum in numbers:
        new_num.append(float(inum))
    numbers = new_num.copy()

            
    action,is_boolean = check_operator_type(packets[opid]['typeid'])
    if is_boolean:
        if action == 'greater than':
            if numbers[0] > numbers[1]:
                value = 1
            else:
                value = 0
        if action == 'less than':
            if numbers[0] < numbers[1]:
                value = 1
            else:
                value = 0
        if action == 'equal to':
            if numbers[0] == numbers[1]:
                value = 1
            else:
                value = 0
    else:
        ## CASE action is_boolean == False
        if action == 'sum':
            value = sum(numbers)
        elif action == 'product':
            value = np.product(numbers)
        elif action == 'minimum':
            value = min(numbers)
        elif action == 'maximum':
            value = max(numbers)

    packets[opid]['value'] = value

    print(opid, packets[opid])
    '''
    for iopid in opids:
        if 'operators' in packets[iopid]:
            if opid in packets[iopid]['operators']:
                if 'literals' not in packets[iopid]:
                    packets[iopid]['literals'] = []
                packets[iopid]['literals'].append(packets[opid]['value'])
     '''     

print(f"Answer: {packets['op0']['value']}")



        

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

