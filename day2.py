import advent_of_code as aoc

## Read in input
num = 2
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]




## PART 1
sub_hor = 0 
depth = 0 
for line in lines: 
    try:  
        int_movement = int(line.split(' ')[1]) 
    except: 
        print(f'something went wrong with {line}')    
        continue 
         
    if 'forward' in line: 
        sub_hor = sub_hor + int_movement 
    elif 'up' in line: 
        depth = depth - int_movement 
    elif 'down' in line: 
        depth = depth + int_movement 
    else: 
       print(f'Input words of forward, up or down not found in {line}. something went wrong') 

print(f'Answer: {sub_hor*depth}')




## PART 2
sub_hor = 0 
aim = 0 
depth = 0 
for line in lines:  
    try:   
        int_movement = int(line.split(' ')[1])  
    except:  
        print(f'something went wrong with {line}')     
        continue  
          
    if 'forward' in line:  
        sub_hor = sub_hor + int_movement 
        depth = depth +  aim * int_movement 
    elif 'up' in line:  
        aim = aim - int_movement 
    elif 'down' in line:  
        aim = aim + int_movement 
    else: 
       print(f'Expected input words not found in {line}. Something went wrong') 

    print(f'horizontal: {sub_hor}, depth: {depth}') 

       
print(f'Answer: {sub_hor*depth}')

