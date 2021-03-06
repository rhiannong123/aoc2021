import advent_of_code as aoc

import pandas as pd


## PART 1
num = 1
lines = aoc.input_readlines(num)
depths = [int(line) for line in lines]

df = pd.DataFrame(depths, columns=['depths'])
df['diff_d'] = df.depths.diff(1)
num_of_inc = df[df.diff_d > 0].shape[0]


## PART 2
df['roll'] = df.depths.rolling(3).sum()
df['diff_roll'] = df.roll.diff(1)
num_of_inc_roll =  df[df.diff_roll > 0].shape[0] 
