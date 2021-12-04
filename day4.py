import advent_of_code as aoc

## Read in input
num = 4
#lines = aoc.input_readlines(num,test=True) # read in test data
lines = aoc.input_readlines(num)
lines = [line.strip('\n') for line in lines]


## PART 1

def check_if_winner(board, called_out):

    ## Check rows
    ## Define row indices
    row_inds_full_row = [
        [ 0, 1, 2, 3, 4],
        [ 5, 6, 7, 8, 9],
        [10,11,12,13,14],
        [15,16,17,18,19],
        [20,21,22,23,24]
        ]

    ## For each list of row indices, check if board row is a subset of called out numbers
    for row_inds in row_inds_full_row:
        check_board = [board[idx] for idx in row_inds] 
        if set(check_board).issubset(set(called_out)):
            ## This board is a winner!
            return True

    ## Check columns
    ## Same logic as rows, just checking the transpose
    col_inds_full_col = [
        [ 0, 5,10,15,20],
        [ 1, 6,11,16,21],
        [ 2, 7,12,17,22],
        [ 3, 8,13,18,23],
        [ 4, 9,14,19,24]
        ]
    for col_inds in col_inds_full_col:
        check_board = [board[idx] for idx in col_inds] 
        if set(check_board).issubset(set(called_out)):
            return True

    ## If no rows or columns wins, return False
    return False



## First line of input is list of bingo numbers called out
## Format to list of integers
call_out = lines.pop(0)
call_out = call_out.split(',')
call_out = [int(inum) for inum in call_out]

lines.pop(0) # Get rid of '' now at top of input

## Define each bingo board as a list of 25 integers
## Create list of boards
boards = []
board = ''
for line in lines:
    if line == '':
        board = board.replace(',',' ').split(' ')
        board = [int(bnum) for bnum in board if bnum != '']
        boards.append(board)
        board = ''
    else:
        board = board + line + ' , '

board = board.replace(',',' ').split(' ')
board = [int(bnum) for bnum in board if bnum != '']
boards.append(board)

## Play bingo
## Keep track of numbers called out
## If a board wins, save board and called out numbers, stop checking
called_out = []
did_it_win = False
for inum in call_out:
    if did_it_win:
        continue
    
    called_out.append(inum)
    
    for board in boards:
        if did_it_win:
            continue
        did_it_win = check_if_winner(board, called_out)
        if did_it_win:
            winning_board = board
            winning_called_out = called_out

sum_not_called_out = sum(inum for inum in winning_board if inum not in winning_called_out)
print(f'Answer: {sum_not_called_out * winning_called_out[-1]}')



## PART 2

## Play bingo
## Keep track of numbers called out
## If a board wins, save board and called out numbers to winning lists
called_out = []
winning_boards = []
winning_called_outs = []
for inum in call_out:    
    called_out.append(inum)

    for board in boards:
        ## Check if already a winner, if so don't update winning lists
        if board in winning_boards:
            continue
        
        did_it_win = check_if_winner(board, called_out)

        if did_it_win:
            ## CASE board won! add it to winning lists
            winning_boards.append(board.copy())
            winning_called_outs.append(called_out.copy())

            
## Get last board to win
winning_board = winning_boards[-1]
winning_called_out = winning_called_outs[-1]

sum_not_called_out = sum(inum for inum in winning_board
                         if inum not in winning_called_out)
print(f'Answer: {sum_not_called_out * winning_called_out[-1]}')

