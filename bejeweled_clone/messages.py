'''
Created on 15 feb 2021
'''
import pygame
from settings import *

class Messages:
    def __init__(self, parent):
        self.surface = parent
        self.title_height = 0
        self.FONT_NORMAL = pygame.font.SysFont("arial", 14)
        self.FONT_TITLE = pygame.font.SysFont("arial", 12)
        self.FONT_ALERT = pygame.font.SysFont("arial", 50)

    def msg_title(self, stage_name):
        label_title = self.FONT_TITLE.render(stage_name, True, FONT_COLOR)
        self.title_height = label_title.get_height()
        self.surface.blit(label_title, (BOX_LEFT, TOPBOX_TOP))
    
    def msg_enemies_list(self, enemies):
        
        lines = ["ENEMIES:"]
        for i, enemy in enumerate(ENEMY_NAMES):
            lines.append(f"{enemy}: {enemies.count(i)}")
        
        h = 0
        for i, line in enumerate(lines):
            label_enemies = self.FONT_NORMAL.render(line, True, FONT_COLOR)
            if h == 0:
                h = label_enemies.get_height()
            self.surface.blit(label_enemies, (BOX_LEFT, MIDBOX_TOP+(h*i+2)))
        
    def msg_current_stats(self, enemy):
        
        lines = [enemy.name, f"HP: {enemy.hp}",f"next weapon atk in {enemy.atk_cooldown}",f"next magic atk in {enemy.magic_cooldown}",f"next special atk in {enemy.special_cooldown}"]
        pygame.draw.rect(self.surface, (105,15,127), (BOX_LEFT+145,MIDBOX_TOP-5, 180,90))
        h = 0
        for i, line in enumerate(lines):
            label_current_enemy = self.FONT_NORMAL.render(line, True, FONT_COLOR)
            if h == 0:
                h = label_current_enemy.get_height()
            self.surface.blit(label_current_enemy, (BOX_LEFT+150, MIDBOX_TOP+(h*i)))
        del lines   
        
        self.surface.blit(enemy.img, (187, 205))
    
    
    def msg_tooltip(self, idx, pos_y, player):
        messages = [f"Gold per bag gem: {player.pouch_amount}", f"Physical damage per sword gem: {player.atk}",
                 f"Physical defense bonus per shield gem: {player.shield}", f"Healing per potion gem: {player.healing}",
                 f"Magic defense bonus per magic shield gem: {player.magic_def}",f"Magic damage per magic gem: {player.magic_atk}",
                 f"Slow seconds per clock gem: {player.magic_slow}",f"Crit chance per gem: {player.crit}"]
        
        label_tooltip = self.FONT_NORMAL.render(messages[idx], True, FONT_COLOR)
        pygame.draw.rect(self.surface, (0,0,0), (BOX_LEFT+30,pos_y+5, label_tooltip.get_width()+20,label_tooltip.get_height()+10))
        self.surface.blit(label_tooltip, (BOX_LEFT+40,pos_y+10))
            
    def msg_upgrades(self, player, IMG_STATS, IMG_DOTS):
        # PLAYER LIFE / GOLD
        lines = [f"HP: {player.current_hp}",f"GOLD: {player.gold}"]
        h = 0
        for i, line in enumerate(lines):
            label_player = self.FONT_NORMAL.render(line, True, FONT_COLOR)
            if h == 0:
                h = label_player.get_height()
            self.surface.blit(label_player, (BOX_LEFT+200, TOPBOX_TOP+(h*i)))
        
        
        self.surface.blit(IMG_STATS, (38,361))
        for i, stat in enumerate(player.all_stats):
            for j in range(stat+1):
                self.surface.blit(IMG_DOTS["g"], (DOTS_LEFT+(DOTS_LEFT_SPACING*j),DOTS_TOP+(DOTS_TOP_SPACING*i)))
            if player.gold >= UPGRADE_PRICE[stat+1]:
                self.surface.blit(IMG_DOTS["up_enable"], (PLUS_LEFT, PLUS_TOP+(PLUS_TOP_SPACING*i)))
            if stat == 9:
                self.surface.blit(IMG_DOTS["up_max"], (PLUS_LEFT, PLUS_TOP+(PLUS_TOP_SPACING*i)))
    
    def display_middle(self, message, y):
        mid = 403+((601-message.get_width())//2)
        self.surface.blit(message,(mid,y))
                    
    def level_up(self, level, stage, bg):
        top = 180
        self.surface.blit(bg,(MARGIN_LEFT,MARGIN_TOP))
        text = self.FONT_ALERT.render(f"LEVEL UP!", True, FONT_COLOR)
        text1 = self.FONT_ALERT.render(f"LEVEL {level+1}: {stage}", True, FONT_COLOR)
        text2 = self.FONT_ALERT.render("GOOD LUCK!", True, FONT_COLOR)
        self.display_middle(text, top)
        self.display_middle(text1, top+text.get_height()+5)
        self.display_middle(text2, top+text.get_height()+5+text2.get_height()+5)
            
    def start(self, bg):
        self.surface.blit(bg,(MARGIN_LEFT,MARGIN_TOP))
        text = self.FONT_ALERT.render("GAME BEGIN NOW", True, FONT_COLOR)
        self.display_middle(text, 180)
        
    def show_killed(self, text):
        line = self.FONT_NORMAL.render(text, True, FONT_COLOR)
        self.surface.blit(line, (38,309))
        
    def show_game_over(self, bg):
        self.surface.blit(bg,(MARGIN_LEFT,MARGIN_TOP))
        text = self.FONT_NORMAL.render("GAME OVER", True, FONT_COLOR)
        text1 = self.FONT_NORMAL.render("[enter] to restart", True, FONT_COLOR)
        self.display_middle(text, 180)
        self.display_middle(text1, 180+5+text.get_height())
        
    def show_game_completed(self, bg):
        self.surface.blit(bg,(MARGIN_LEFT,MARGIN_TOP))
        text = self.FONT_NORMAL.render("YOU BEAT THE GAME", True, FONT_COLOR)
        text1 = self.FONT_NORMAL.render("[enter] to restart", True, FONT_COLOR)
        self.display_middle(text, 180)
        self.display_middle(text1, 180+5+text.get_height())
    
