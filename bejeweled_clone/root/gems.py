from PyMatch3 import IMAGES
import random
from settings import * 

class Gem:
    def __init__(self, color, x=0, y=0):
        self.color = color
        self.x = x
        self.y = y
        self.type= "regular"
        self.angle = 0
        self.action = "none"
        self.set_img()
        
    def set_img(self):
        self.img = IMAGES[self.color]
        
    def convert_special(self):
        self.type="special"
        if "2" not in self.color: 
            self.color+="2"
        self.set_img()
        
    def convert_bomb(self):
        self.type="bomb"
        self.color="x"
        self.set_img()
        
    def convert_destroyed(self, ypos):
        self.color = random.choice(JEWELS[:7])
        self.set_img()
        self.y = ypos
        
    def mark_destroy(self):
        self.action="destroy"
        self.type="regular"
        self.color = self.color
        self.set_img()
     
    def set_coords(self, newx, newy):
        self.x = newx
        self.y = newy 

        
def update_gems(board):
    for row in range(ROW_N):
        
        for col in range(COL_N):
            board[row][col].set_coords(col*60, row*60)
            
def get_specials(board):
    specials = []
    
    for row in range(ROW_N):
        
        for col in range(COL_N):       
            gem = board[row][col]
            
            if gem.type=="special":
                specials.append(gem.color)
                
    return specials

def assign_specials(board, specials):
    for special in specials:
        
        changed = 0
        for row in range(ROW_N):
            
            for col in range(COL_N):
                gem = board[row][col]
                
                if gem.color == special and gem.type == "regular":
                    gem.convert_special()
                    changed = 1
                    
            if changed == 1:
                break