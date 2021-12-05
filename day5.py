import pandas as pd

import advent_of_code as aoc

## Read in input
num = 5
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]
verbose = False



## Functions ##################################################
def check_for_diag(line):
    ''' line = [x1,y1,x2,y2], each entry an int
    '''
    x1,y1,x2,y2 = line

    if (x1 != x2) and (y1 != y2):
        if verbose:
            print(f'{x1} != {x2}, {y1} != {y2}. Diagonal found')
        ## CASE: diagonal line
        return True
    else:
        ## CASE: vertical, horizontal, single point
        return False 


    
def check_for_diag_45(line):
    ''' line = [x1,y1,x2,y2], each entry an int
        45 deg angle would mean lines of y=x+constant, y=-x+constant

        returns: Either: 
                  True, m, b if 45 deg angle # y = mx + b
                  False, 0, 0
    '''
    x1,y1,x2,y2 = line

    ## Check line y = x + b (m = 1)
    ##  also: y = -x + b (m = -1)
    b_posm = y1 - x1
    b_negm = y1 + x1
    if (y2 == x2 + b_posm):
        ## CASE line satisfies slope of 1
        return True, 1, b_posm
    elif (y2 == -x2 + b_negm):
        ## CASE line satisfies slope of -1
        return True, -1, b_negm
    else:
        ## CASE not 45
        return False, 0, 0
    

## PART 1  ##################################################


    
## Go through input, get highest x, highest y
xs = [] 
ys = []
linesss = []
for line in lines: 
    init,final = line.split(' -> ') 
    x1,y1 = init.split(',') 
    x1 = int(x1) 
    y1 = int(y1) 
    x2,y2 = final.split(',') 
    x2 = int(x2) 
    y2 = int(y2) 
    xs.append([x1,x2]) 
    ys.append([y1,y2])
    linesss.append([x1,y1,x2,y2])

maxx = max([max(i_xs) for i_xs in xs])
maxy = max([max(i_ys) for i_ys in ys])

## Build dataframe to use as grid
cols = [str(x) for x in range(maxx+1)]
df = pd.DataFrame(0,index=range(maxy+1),columns=cols) 

## Go through line by line, update grid,
##  and if lines pass condition,
##  increment where lines cover the grid
for line in linesss:
    ## Skip diagonal lines
    if check_for_diag(line):
        continue
    else:
        if verbose:
            print(f'{line} not diagonal, continuing')

    x1,y1,x2,y2 = line

    if (y1 == y2):
        ## is x1 or x2 bigger?
        iminx = min(x1,x2)
        imaxx = max(x1,x2)
        
        ## Horizontal, iterate over columns
        for col in range(iminx,imaxx+1):
            strcol = str(col)
            df.loc[y1,strcol] = df.loc[y1,strcol] + 1
        
    
    if (x1 == x2):
        ## is y1 or y2 bigger?
        iminy = min(y1,y2)
        imaxy = max(y1,y2)
        
        ## Vertical, iterate over rows
        for row in range(iminy,imaxy+1):
            strx = str(x1)
            df.loc[row,strx] = df.loc[row,strx] + 1

## Count any danger, spots where dataframe >= 2
danger_count = (df >= 2).sum().sum()  
print(f'Answer: {danger_count}')




## PART 2  ##################################################

## Go through input, get highest x, highest y
xs = [] 
ys = []
linesss = []
for line in lines: 
    init,final = line.split(' -> ') 
    x1,y1 = init.split(',') 
    x1 = int(x1) 
    y1 = int(y1) 
    x2,y2 = final.split(',') 
    x2 = int(x2) 
    y2 = int(y2) 
    xs.append([x1,x2]) 
    ys.append([y1,y2])
    linesss.append([x1,y1,x2,y2])

maxx = max([max(i_xs) for i_xs in xs])
maxy = max([max(i_ys) for i_ys in ys])

## Build dataframe to use as grid
cols = [str(x) for x in range(maxx+1)]
df = pd.DataFrame(0,index=range(maxy+1),columns=cols) 

## Go through line by line, update grid,
##  and if lines pass condition,
##  increment where lines cover the grid
for line in linesss:
    ## Determine if horizontal, vertical, 45 deg diagonal or none
    x1,y1,x2,y2 = line
    check_45 = check_for_diag_45(line)
    
    if (y1 == y2):
        state = 'horizontal'
    elif (x1 == x2):
        state = 'vertical'
    elif check_45[0]:
        state = '45diagonal'
        slope = check_45[1]
        b = check_45[2]
    else:
        ## CASE line is not valid, continue
        continue

    ## is x1 or x2 bigger? is y1 or y2 bigger?
    iminx = min(x1,x2)
    imaxx = max(x1,x2)
    iminy = min(y1,y2)
    imaxy = max(y1,y2)

    if state == 'horizontal':
        ## Horizontal, iterate over columns
        for col in range(iminx,imaxx+1):
            strcol = str(col)
            df.loc[y1,strcol] = df.loc[y1,strcol] + 1
    
    if state == 'vertical':
        ## Vertical, iterate over rows
        for row in range(iminy,imaxy+1):
            strx = str(x1)
            df.loc[row,strx] = df.loc[row,strx] + 1

    if state == '45diagonal':
        if slope == 1:
            for col in range(iminx,imaxx+1):
                ## y = x + b
                strcol = str(col)
                row = col + b 
                df.loc[row,strcol] = df.loc[row,strcol] + 1        
        else:
            ## CASE slope == -1
            for col in range(iminx,imaxx+1):
                ## y = -x + b
                strcol = str(col)
                row = b - col 
                df.loc[row,strcol] = df.loc[row,strcol] + 1        

## Build dataframe to use as grid
danger_count = (df >= 2).sum().sum() 

print(f'Answer: {danger_count}')
