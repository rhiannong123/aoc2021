import advent_of_code as aoc

## Read in input
num = 3
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]


## PART 1

# Get length of line, based on first entry
length = len(lines[0])

gamma_rate = ''
epsilon_rate = ''
for idx in range(length):

    # List of bit for consideration (first entry in each line, second entry in each line)
    # Sum up ones and zeros
    bits = [line[idx] for line in lines]
    ones = [1 for bit in bits if bit == '1']
    zeros = [1 for bit in bits if bit == '0']

    if sum(ones) > sum(zeros):
        gamma_rate = gamma_rate + '1'
        epsilon_rate = epsilon_rate + '0'
    else:
        gamma_rate = gamma_rate + '0'
        epsilon_rate = epsilon_rate + '1'
print(gamma_rate)
print(epsilon_rate)        

# Convert binaries to decimals and get the product
print(f'Answer: {int(gamma_rate,2)*int(epsilon_rate,2)}')





## PART 2
# Get length of line, based on first entry
length = len(lines[0])

# Start with copy of all lines, whiddle down list based on most common or least common
#   digit for each entry in each line
ox = lines.copy()
co2 = lines.copy()

# Oxygen for loop
for idx in range(length): 
    if len(ox) == 1: 
        continue 

    # List of bit for consideration (first entry in each line, second entry in each line)
    # Sum up ones and zeros
    bits = [line[idx] for line in ox] 
    ones = [1 for bit in bits if bit == '1'] 
    zeros = [1 for bit in bits if bit == '0'] 
 
    print(sum(ones), sum(zeros)) 
     
    if sum(ones) >= sum(zeros): 
        ox = [line for line in ox if line[idx] == '1'] 
    else: 
        ox = [line for line in ox if line[idx] == '0']

# CO2 for loop
for idx in range(length): 
    if len(co2) == 1: 
        continue 
     
    # List of bit for consideration (first entry in each line, second entry in each line)
    # Sum up ones and zeros
    bits = [line[idx] for line in co2] 
    ones = [1 for bit in bits if bit == '1'] 
    zeros = [1 for bit in bits if bit == '0'] 
 
    print(sum(ones), sum(zeros)) 
     
    if sum(ones) < sum(zeros): 
        co2 = [line for line in co2 if line[idx] == '1'] 
    else: 
        co2 = [line for line in co2 if line[idx] == '0'] 

print(ox)
print(co2)     

# Convert binaries to decimals and get the product
print(f'Answer: {int(ox[0],2)*int(co2[0],2)}')


