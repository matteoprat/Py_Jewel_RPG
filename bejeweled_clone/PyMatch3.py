import random
import rpg
import board
import score
import gems
import messages
import pygame
from pygame.locals import *
from settings import *

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("RPyGjeweled")
surface = pygame.display.set_mode(size=(BOARD_WIDTH, BOARD_HEIGHT))
IMAGES = {k:pygame.image.load(f"assets/jewel_{k}.png").convert_alpha() for k in JEWELS}
IMG_DOTS = {k:pygame.image.load(f"assets/{v}.png").convert_alpha() for k, v in LVL_GFX.items()}
IMG_STATS = pygame.image.load("assets/gem_levels.png").convert_alpha()
IMG_ENEMIES = [pygame.image.load(f"assets/enemies/{k}.png").convert_alpha() for k in ENEMY_NAMES]
BG_TEXT = pygame.image.load("assets/bgtext.png").convert_alpha()
    

class Game:
    def __init__(self, parent):
        self.board = board.create_new_board()
        self.all_gems = self.get_all_gems()
        self.surface = parent
        self.bg = pygame.image.load("assets/bg.png").convert()
        self.level_hint = 3
        self.level=0
        self.player = rpg.Player()
        self.enemies = self.new_level()
        self.spawn_enemy()
        self.msg = messages.Messages(self.surface)
        self.enemy_killed_msg = ""
        self.enemy_killed_cooldown = 0
        self.level_start = True
        self.level_up = False
        self.level_up_cooldwon = 30*3
        self.start = 30*2
        self.pause = False
        self.display_hint = False
    
    def reset_game(self):
        self.reset_board()
        del self.player
        self.level_start = True
        self.level_up = False
        self.level_up_cooldwon = 30*3
        self.start = 30*2
        self.pause = False
        self.level_hint = 3
        self.level=0
        self.player = rpg.Player()
        self.enemies = self.new_level()
        self.spawn_enemy()
    
    def get_all_gems(self):
        gems = []
        for row in range(ROW_N):
            
            for col in range(COL_N):
                gems.append(self.board[row][col])
                
        return gems  

    def get_mouse_block(self):
        x,y = pygame.mouse.get_pos()
        return ((x-MARGIN_LEFT)//60,(y-MARGIN_TOP)//60)
    
    def new_level(self):
        self.stagename = f"LEVEL {self.level+1}: {STAGE_NAME[self.level]}"
        self.level_hint = 3
        return [n for n in LEVELS[self.level]]
              
    def spawn_enemy(self):
        self.enemy = rpg.Enemy(self.enemies[0], IMG_ENEMIES[self.enemies[0]])
    
    def debug(self):
        for row in range(ROW_N):
            o=""
            
            for col in range(COL_N):
                o+= self.board[row][col].color if self.board[row][col].action != "destroy" else "D"
            
            print(o)
        
    def draw_board(self):
        
        self.surface.blit(self.bg,(0,0))
        if self.display_hint:
            self.show_hint()
        self.msg.msg_upgrades(self.player, IMG_STATS, IMG_DOTS)
        if self.pause == False:    
            self.msg.msg_title(self.stagename)
            self.msg.msg_enemies_list(self.enemies)           
            self.msg.msg_current_stats(self.enemy)
        
        for row_n, row in enumerate(self.board):
            
            for col_n, gem in enumerate(row):
                if (col_n, row_n)== self.get_mouse_block():
                    pygame.draw.rect(self.surface,(255,255,255),(MARGIN_LEFT+gem.x,MARGIN_TOP+gem.y,60,60), 2)
                    
                if gem.action=="destroy":
                    img = pygame.transform.rotate(gem.img,gem.angle)
                
                else:
                    img = gem.img
                    
                self.surface.blit(img,(MARGIN_LEFT+gem.x,MARGIN_TOP+gem.y))
    
    def play_sound(self, sound_name):
        sound = pygame.mixer.Sound("audio/"+sound_name+".wav")
        pygame.mixer.Sound.play(sound)
                        
    def play_move(self, old, new):
        self.display_hint = False
        # GETTING DATA FOR SWAP
        old_gem = self.board[old[1]][old[0]]                
        new_gem = self.board[new[1]][new[0]]
         
        self.gems_swap_transition(old_gem, new_gem, old[1], new[1], old[0], new[0])
        
        # SWAPPING gems on the grid
        self.board[old[1]][old[0]] = new_gem
        self.board[new[1]][new[0]] = old_gem
        
        if self.move_happened(old_gem, new_gem) == False:
            self.gems_swap_transition(old_gem, new_gem, new[1], old[1], new[0], old[0])
            
            # SWAPPING gems back on the grid
            self.board[old[1]][old[0]] = old_gem
            self.board[new[1]][new[0]] = new_gem    
    
    def move_happened(self, gem, new_gem):
        coords = [(gem.x//60,gem.y//60),(new_gem.x//60,new_gem.y//60)]
               
        row_affected = board.check_match_row(self.board, coords, True)
        col_affected = board.check_match_col(self.board, coords, True)
        
        # IF change occurred return TRUE else FALSE
        if len(row_affected)>0 or len(col_affected)>0 or gem.type=="bomb":
            scores = {k:0 for k in JEWELS[:8]}
            while len(row_affected)>0 or len(col_affected)>0 or gem.type=="bomb":
                self.play_sound("match")
                if gem.type == "bomb":
                    self.detonate_bomb(new_gem.color)
                    gem.mark_destroy()
                        
                self.mark_destroy(row_affected)
                self.mark_destroy(col_affected)
                
                for gem in self.all_gems:
                    if gem.action == "destroy" and gem.color[0] in JEWELS[:8]:
                        scores[gem.color[0]]+=1
                
                self.gem_destroy_transition()
                self.update_destroyed()
                
                #self.debug()
                
                row_affected = board.check_match_row(self.board)
                col_affected = board.check_match_col(self.board)
            
            result = score.calculate_score(scores, self.player, self.enemy)
            # result is -1 if the enemy is alive otherwise it contain a message
            if result != -1:
                self.enemy_killed_msg = result
                self.enemy_killed_cooldown = 30*2
                self.player.gold += self.enemy.gold
                self.enemies.pop(0)
                del self.enemy
                # check if the level have other enemies
                if len(self.enemies) > 0:
                    self.spawn_enemy()
                else:
                    self.level_up = True
                    self.level+=1
                    # check if current stage is < than max stage
                    if len(LEVELS) > self.level:
                        self.play_sound("stage_clear")                        
                        self.player.level_up(self.level)
                        self.enemies = self.new_level()
                        self.spawn_enemy()
                    else:
                        self.pause = True
            
            if board.board_have_moves(self.board) == False:
                self.reset_board()
            
            return True
            
        else:
            return False

    def detonate_bomb(self, color):
        for gem in self.all_gems:
            
            if gem.color[0] == color[0]:
                gem.mark_destroy()
    
    def mark_destroy(self, gems):
        for gem in gems:
            gem.mark_destroy()
    
    def update_destroyed(self):
        newy = -60
        # we initialize a dictionary containing columns and number of shifts
        # per columns
        vpos = {k:1 for k in range(COL_N)}
        
        for row in range(ROW_N-1, -1, -1):
            
            for col in range(COL_N):
                gem = self.board[row][col]
                
                while gem.color == "empty": # kind of bubble sort algorithm
                    gem.convert_destroyed(newy*vpos[col])
                    vpos[col]+=1
                    start_row = row
                    
                    while start_row > 0:
                        self.board[start_row][col], self.board[start_row-1][col] = self.board[start_row-1][col], self.board[start_row][col]  
                        start_row -= 1
                        
                    gem = self.board[row][col]
                    
        self.gems_falling_transition()

    def gems_swap_transition(self, old_gem, new_gem, old_board_y, new_board_y, old_board_x, new_board_x):
        # transition graphic
        i = 1
        while i <= 60:
            modifier = (10, -10)
            
            if old_board_y != new_board_y:
                     
                if old_board_y > new_board_y: # it moves from right to left
                    modifier = (-10, 10)
                    
                old_gem.y += modifier[0]
                new_gem.y += modifier[1]
                
            else:
                if old_board_x > new_board_x: # it moves from bottom to top
                    modifier = (-10, 10)
                    
                old_gem.x += modifier[0]
                new_gem.x += modifier[1]
            
            i += 10
            
            self.draw_board()
            pygame.display.update()
            FPSCLOCK.tick(30)
    
    def gem_destroy_transition(self):
        for frame in range(8):
            
            for gem in self.all_gems:
                
                if gem.action == "destroy":
                    gem.angle = 15+(15*frame)
                    
                    if frame == 7:
                        gem.color = "empty"
                         
            self.draw_board()
            pygame.display.update()
            FPSCLOCK.tick(30)        
        
        for gem in self.all_gems:
            gem.angle = 0
            gem.action = "none"
        
    def gems_falling_transition(self):
        falling = 1
        while falling == 1:
            
            falling = 0
            for row in range(ROW_N):
                
                for col in range(COL_N):
                    gem = self.board[row][col]
                    
                    if gem.y != row*60:
                        falling = 1
                        gem.y+=20
                        
            self.draw_board()
            pygame.display.update()
            FPSCLOCK.tick(30)
    
    def reset_board(self):
        specials = gems.get_specials(self.board)
        
        board.delete_board(self.board)
        
        self.board = board.create_new_board()
        self.all_gems = self.get_all_gems()
        
        self.draw_board()
        
        gems.assign_specials(self.board, specials)
       
    def buy_upgrade(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # s = top; e = bottom; d = distance from top and next top 
        s,e,d = (367.5,394.5,48)
        
        if PLUS_LEFT < mouse_x <= 330:
            for i, stat in enumerate(self.player.all_stats):
                if stat < len(UPGRADE_PRICE)-1:
                    if self.player.gold >= UPGRADE_PRICE[stat+1] and s+(d*i) < mouse_y < e+(d*i):
                        self.player.upgrade_item(i)
                        self.play_sound("upgrade") 

    def show_hint(self):
        ''' Get the first move available, draw a green rectangle around gem '''
        coords = board.board_have_moves(self.board)
        pygame.draw.rect(self.surface,(0,255,0),(MARGIN_LEFT+(coords[1][1]*60),MARGIN_TOP+(coords[1][0]*60),60,60), 2)
        
    def show_tooltip(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # s = top; e = bottom; d = distance from top and next top
        s,e,d=(361,402,47)
        stats = {(s+(d*i),e+(d*i)):i for i in range(8)}
        if 38 < mouse_x < 78:
            for k in stats:
                if k[0] < mouse_y < k[1]:
                    self.msg.msg_tooltip(stats[k], k[0], self.player)

    def run(self):
        pygame.mixer.music.load("audio/pygem.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops = -1)
        running = True
        mousepos = self.get_mouse_block()
        self.draw_board()
        
        while board.board_have_moves(self.board) == False:
            self.board = board.create_new_board()
        
        mousedown = False
        while running:
            for event in pygame.event.get():
                        
                        if event.type == QUIT:
                            running = False
                                          
                        if event.type == KEYDOWN:                        
                            if event.key == K_ESCAPE:
                                running = False
                            
                            if event.key == K_h:
                                
                                if self.level_hint > 0:
                                    self.display_hint = True
                                    self.level_hint -= 1
                                else:
                                    print("USER HAVE NO HINT LEFT FOR THIS LEVEL")
                                    
                            if event.key == K_r:
                                self.reset_board()
                                
                            if self.pause == True and event.key == K_RETURN:
                                self.reset_game()
                                self.pause = False
                        
                        if self.pause == False:
                        
                            if event.type == MOUSEMOTION:
                                
                                if mousedown == True:
                                    newpos = self.get_mouse_block()
                                    if newpos != mousepos:
                                        
                                        if abs(mousepos[0]-newpos[0]) < 2 and abs(mousepos[1]-newpos[1] < 2) and -1 < newpos[0] < COL_N and -1 < newpos[1] < ROW_N:
                                            self.play_move(mousepos, newpos)
                                            mousedown = False
                                    
                                mousepos = self.get_mouse_block()
                                self.draw_board()
                                
                            if event.type == MOUSEBUTTONDOWN:
                                self.buy_upgrade()
                                mousedown = True
                                mousepos = self.get_mouse_block()
                                
                            if event.type == MOUSEBUTTONUP:
                                mousedown = False
            
            if self.pause == False:
                if self.player:
                    self.player.turn()
            
                if self.enemy:
                    self.player.get_damage(self.enemy.turn())
                else:
                    self.level+=1
                    self.new_level()
            
            self.draw_board()    
            
            if self.player.current_hp <= 0:
                self.pause = True
                self.msg.show_game_over(BG_TEXT)
                self.play_sound("game_over")
            
            if self.enemy_killed_cooldown > 0:
                self.msg.show_killed(self.enemy_killed_msg)
                self.enemy_killed_cooldown -= 1
                if self.enemy_killed_cooldown == 0:
                    self.enemy_killed_msg = ""
            
            if self.level_up:
                self.level_up_cooldwon-=1
                if self.level == len(LEVELS):
                    self.msg.show_game_completed(BG_TEXT)
                else:
                    self.msg.level_up(self.level, STAGE_NAME[self.level], BG_TEXT)
                    if self.level_up_cooldwon == 0:
                        self.level_up_cooldwon = 30*2
                        self.level_up = False
            if self.start > 0:
                self.msg.start(BG_TEXT)
                self.start-=1
            
            self.show_tooltip()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    a=Game(surface)
    a.run()