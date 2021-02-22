import random, pygame
from settings import *
import gems
#from PyMatch3 import IMAGES

def delete_board(board):
    for row in range(ROW_N):
        
        for col in range(COL_N):
            gem = board[row][col]
            del gem
 
def create_new_board():
    ''' this will create a grid 8x8 filled with random jewels
        so that we have something like:
        [['o', 'c', 'o', 'r', 'r', 'p', 'g', 'r'], 
         ['r', 'b', 'b', 'b', 'o', 'b', 'c', 'b'], 
         ['o', 'o', 'r', 'g', 'y', 'p', 'p', 'c'], 
         ['b', 'o', 'p', 'y', 'y', 'y', 'v', 'y'], 
         ['v', 'g', 'v', 'y', 'o', 'y', 'r', 'b'], 
         ['g', 'g', 'o', 'y', 'v', 'c', 'y', 'c'], 
         ['r', 'r', 'o', 'y', 'c', 'o', 'g', 'b'], 
         ['p', 'p', 'c', 'r', 'b', 'b', 'r', 'g']]
    '''
    grid = []

    for row in range(ROW_N):
        
        last_color = ""
        equals_letter_count = 0
        rows = []
        
        for col in range(COL_N):
            color = random.choice(JEWELS[:8])
                        
            if color == last_color:
                equals_letter_count += 1
                
                if equals_letter_count >= 2:
                    color = JEWELS[(JEWELS.index(color)+1)%8]
                    equals_letter_count = 0
            
            if row >= 2:
                
                if color == grid[row-2][col].color and color == grid[row-1][col].color:
                    color = JEWELS[(JEWELS.index(color)+1)%8]
            
            last_color = color
            rows.append(gems.Gem(color, 60*col, 60*row))
        
        grid.append(rows)
        
    return grid
    
def is_valid(board, a,b,c):
    return board[a[0]][a[1]].color == board[b[0]][b[1]].color == board[c[0]][c[1]].color                                                                    
    
def board_have_moves(board):
    ''' a valid move is when we can have 3 or more adjacent piece of same type
        by moving a piece, so I check for:
        
        HORIZONTAL CONTROLS: these perform each cycle, inner from 0 to len -4
        XX.X    X.XX   
        
        HORIZONTAL MULTILINE CONTROLS: these perform from 0 to len -2, inner from 0 to len -3
        X..    ..X   .XX  XX.   .X.  X.X 
        .XX    XX.   X..  ..X   X.X  .X.
        
        VERTICAL CONTROLS: these perform from 0 to len -4
        X  X   
        X  .
        .  X
        X  X
        
        VERTICAL MULTICOLUMS CONTROLS: these perform  from 0 to len -3, inner from 0 to len -2
        X    .X   X.  .X   .X   X.   
        X    .X   .X  X.   X.   .X
        .X   X.   X.  .X   X.   .X
    '''
    vsize = ROW_N
    hsize = COL_N
    for i in range(vsize):
        
        for j in range(hsize):
            
            if j <= hsize-4:
                # horizontal controls
                if is_valid(board, (i,j),(i,j+1),(i,j+3)):
                    return True, (i,j+3)
                elif is_valid(board, (i,j), (i,j+2), (i,j+3)):
                    return True, (i,j)
            
            if j <= hsize-3 and i <= vsize -2: 
                # horizontal multiline controls
                if is_valid(board, (i,j),(i+1,j+1),(i+1,j+2)):
                    return True, (i,j)
                elif is_valid(board, (i+1,j),(i+1,j+1),(i,j+2)):
                    return True, (i,j+2)
                elif is_valid(board, (i+1,j),(i,j+1),(i,j+2)):
                    return True, (i+1,j)
                elif is_valid(board, (i,j),(i,j+1),(i+1,j+2)):
                    return True, (i+1,j+2)
                elif is_valid(board, (i+1,j),(i,j+1),(i+1,j+2)):
                    return True, (i,j+1)
                elif is_valid(board, (i,j),(i+1,j+1),(i,j+2)):
                    return True, (i+1, j+1)
            
            if i <= vsize-4:
                # vertical controls
                if is_valid(board, (i,j),(i+1,j),(i+3,j)):
                    return True, (i+3,j)
                elif is_valid(board, (i,j),(i+2,j),(i+3,j)):
                    return True, (i,j)
                        
            if i <= vsize-3 and j <= hsize-2:
                # vertical multicolumns control
                if is_valid(board, (i,j),(i+1,j),(i+2,j+1)):
                    return True, (i+2,j+1)
                if is_valid(board, (i,j+1),(i+1,j+1),(i+2,j)):
                    return True, (i+2,j)
                if is_valid(board, (i,j),(i+1,j+1),(i+2,j)):
                    return True, (i+1, j+1)
                if is_valid(board, (i,j+1),(i+1,j),(i+2,j+1)):
                    return True, (i+1, j)
                if is_valid(board, (i,j+1),(i+1,j),(i+2,j)):
                    return True, (i,j+1)
                if is_valid(board, (i,j),(i+1,j+1),(i+2,j+1)):
                    return True, (i,j)
            
    return False

def mark_for_destruction(board, special, count, tmp, what):
    affected=[]
    
    if count >= 3:
        
        if len(special) > 0:
            
            if what == "col":
                for col in special:
                    for row in range(ROW_N):
                        if board[row][col].color != "x":
                            board[row][col].action="destroy"
            
            elif what == "row":
                for row in special:
                    for col in range(COL_N):
                        if board[row][col].color != "x":
                            board[row][col].action="destroy"
                            
        affected.extend(tmp)
    
    return affected

def check_match_row(board, coords=[(-1,-1),(-1,-1)], played=False):
    affected = []
    
    for row in range(ROW_N):
        
        last=""
        count=1
        special=[]
        tmp=[]
        
        for col in range(COL_N):
            
            gem=board[row][col]
            
            if gem.color[0] == last:
                count+=1
                tmp.append(gem)
                
                if gem.type=="special":
                    special.append(col)
                
                if count == 5:
                    if played:
                        if coords[0][1] == row:
                            thisgem = board[coords[0][1]][coords[0][0]]
                        elif coords[1][1] == row:
                            thisgem = board[coords[1][1]][coords[1][0]]
                    else:
                        thisgem = gem
                    if thisgem in tmp:        
                        tmp.remove(thisgem)
                    else:
                        tmp.remove(gem)
                    thisgem.convert_bomb()
                
                if count == 4:
                    if played:
                        if coords[0][1] == row:
                            thisgem = board[coords[0][1]][coords[0][0]]
                        elif coords[1][1] == row:
                            thisgem = board[coords[1][1]][coords[1][0]]
                    else:
                        thisgem = gem
                    if thisgem in tmp:        
                        tmp.remove(thisgem)
                    else:
                        tmp.remove(gem)
                    thisgem.convert_special()
                    
                if col == COL_N-1:
                    affected.extend(mark_for_destruction(board, special, count, tmp, what="col"))
                    tmp.clear()
            
            else:
                affected.extend(mark_for_destruction(board, special, count, tmp, what="col"))
                tmp.clear()
                tmp.append(gem)
                count = 1
                special.clear()
            last = gem.color[0]
    
    return affected
            
def check_match_col(board, coords=[(-1,-1),(-1,-1)], played=False):
    affected = []
    
    for col in range(COL_N):
        
        last=""
        count=1
        special = []
        tmp = []
        
        for row in range(ROW_N):
            gem=board[row][col]
                
            if gem.color[0] == last:
                count+=1
                tmp.append(gem)
                
                if gem.type=="special":
                    special.append(row)
                
                if count == 5:
                    if played:
                        if coords[0][0] == col:
                            thisgem = board[coords[0][1]][coords[0][0]]
                        elif coords[1][0] == col:
                            thisgem = board[coords[1][1]][coords[1][0]]
                    else:
                        thisgem = gem
                    if thisgem in tmp:        
                        tmp.remove(thisgem)
                    else:
                        tmp.remove(gem)
                    thisgem.convert_bomb()
                
                if count == 4:
                    if played:
                        if coords[0][0] == col:
                            thisgem = board[coords[0][1]][coords[0][0]]
                        elif coords[1][0] == col:
                            thisgem = board[coords[1][1]][coords[1][0]]
                    else:
                        thisgem = gem
                    if thisgem in tmp:        
                        tmp.remove(thisgem)
                    else:
                        tmp.remove(gem)
                    thisgem.convert_special()

                if row == ROW_N-1:
                    affected.extend(mark_for_destruction(board, special, count, tmp, what="row"))
                    tmp.clear()
                
            else:
                affected.extend(mark_for_destruction(board, special, count, tmp, what="row"))
                tmp.clear()
                tmp.append(gem)
                count = 1
                special.clear()
            
            last = gem.color[0]
           
    return affected