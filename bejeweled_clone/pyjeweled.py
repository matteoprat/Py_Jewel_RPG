import random
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Pyjeweled")
surface = pygame.display.set_mode(size=(480, 480))

JEWELS = list("gbrpyvoc")
IMAGES = {k:pygame.image.load(f"assets/jewel_{k}.png").convert_alpha() for k in JEWELS}

def create_grid():
    # this function create a 8x8 grid filled with random jewels
    grid = []
    # just filling the grid
    for _ in range(8):
        row = []
        for _ in range(8):
            row.append(random.choice(JEWELS))
        grid.append(row)
    # control if it have 3 or more identical gems close to each other, in that case it rebuild the grid
    if check_have_adjacent(grid):
        return create_grid()
    # control if the grid have at least 1 move available, if not, rebuild the grid
    if check_moves(grid) == False:
        return create_grid()
    # once it pass all controls, return the valid grid to the player
    return grid

def check_have_adjacent(grid):
    rows = check_have_adjacent_rows(grid)
    cols = check_have_adjacent_cols(grid)
    if rows == True or cols == True:
        return True
    return False
    
def check_have_adjacent_rows(grid):
    ''' count if there are at least 3 adjacent gems of the same kind close to each other in rows '''
    for line in grid:
        equalcount = 1
        last = ""
        for c in line:
            if c.lower() == last:
                equalcount += 1
            else:
                equalcount = 1
            if equalcount >= 3:
                return True
            last = c.lower()
    return False

def check_have_adjacent_cols(grid):
    ''' count if there are at least 3 adjacent gems of the same kind close to each other in columns '''
    for i in range(8):
        equalcount = 1
        last = ""
        for j in range(8):
            if grid[j][i].lower() == last:
                equalcount += 1
            else:
                equalcount = 1
            if equalcount >= 3:
                return True
            last = grid[j][i].lower()
    return False
    
def check_moves(grid):
    if check_moves_rows(grid) or check_moves_cols(grid):
        return True
    return False

def check_moves_rows(grid):
    for row in grid:
        for i in range(1,6):
            if row[i-1].lower() == row[i].lower() and row[i+2].lower() == row[i].lower():
                return True
    return False

def check_moves_cols(grid):
    for i in range(8):
        for j in range(1,6):
            if grid[j-1][i].lower() == grid[j][i].lower() and grid[j+2][i].lower() == grid[j][i].lower():
                return True
    return False

def display_grid(grid, parent, bg, pos):
    parent.blit(bg,(0,0))
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if (j,i)==pos:
                pygame.draw.rect(surface,(255,0,0),(i*60,j*60,60,60), 2)
            parent.blit(IMAGES[col],(j*60,i*60))

def play_move(grid, oldpos, newpos):
    color = grid[oldpos[0]][oldpos[1]]
    grid[oldpos[0]][oldpos[1]],grid[newpos[0]][newpos[1]]=grid[newpos[0]][newpos[1]],grid[oldpos[0]][oldpos[1]]
    grid = check_move(grid, newpos,color)
    return grid

def count_adjacent(sequence, color):
    out = 0
    for i in range(5,2,-1):
        if color*i in sequence:
            out = i
            break
    return out

def redraw_grid(grid):
    newcols = []
    for i in range(8):
        col = "".join(grid[j][i] for j in range(8) if grid[j][i] != "0")
        l = len(col)
        if l < 8:
            pre = ""
            for i in range(8-l):
                pre+=random.choice(JEWELS)
            col = pre+col
        newcols.append(col)
    newgrid = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append(newcols[j][i])
        newgrid.append(row)
    return newgrid

def check_move(grid, pos,color):
    y,x = pos[0],pos[1]
    # check the row
    row = "".join(grid[y])
    rowcount = count_adjacent(row, color)    
    col = "".join([grid[i][x] for i in range(8)])
    colcount = count_adjacent(col, color)
    row = row.replace(color*rowcount,"0"*rowcount)
    col = col.replace(color*colcount,"0"*colcount)
    # update
    if rowcount + colcount > 0:
        for i in range(8):
            grid[y][i] = row[i]
        for i in range(8):
            grid[i][x] = col[i]
        grid = redraw_grid(grid)
    print(grid)
    return grid
    
mygrid = create_grid()
print("  |",*list("ABCDEFGH"))
print("-"*19)
for i, row in enumerate(mygrid):
    print(i+1,"|",*(row))


bg = pygame.image.load("assets/bg.png")
running = True
mousepos = pygame.mouse.get_pos()
mousepos = (mousepos[1]//60, mousepos[0]//60)
display_grid(mygrid, surface,bg, mousepos)
FPS = 30
FPSCLOCK = pygame.time.Clock()
down = False
while running:
    for event in pygame.event.get():
                                  
                if event.type == KEYDOWN:                        
                    if event.key == K_ESCAPE:
                        running = False
                
                if event.type == MOUSEMOTION:
                    if down == True:
                        newpos = pos = pygame.mouse.get_pos()
                        newpos = (newpos[1]//60, newpos[0]//60)
                        if newpos != mousepos:
                            if abs(mousepos[0]-newpos[0]) < 2 and abs(mousepos[1]-newpos[1] < 2):
                                play_move(mygrid,mousepos,newpos)
                                down = False
                        
                    pos = pygame.mouse.get_pos()
                    pos = (pos[1]//60, pos[0]//60)
                    display_grid(mygrid, surface,bg, pos)
                    
                if event.type == MOUSEBUTTONDOWN:
                    down = True
                    pos = pygame.mouse.get_pos()
                    mousepos = (pos[1]//60, pos[0]//60)
                    
                if event.type == MOUSEBUTTONUP:
                    down = False
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)
