'''
Created on 3 feb 2021
'''
import pygame
from pygame.locals import *

JEWELS = ["g", "b", "r", "p", "y", "v", "o", "c",
          "g2", "b2", "r2", "p2", "y2", "v2", "o2", "c2",
          "x", "empty"
          ] 

BOARD_WIDTH = 1024
BOARD_HEIGTH = 768

MARGIN_TOP = 24
MARGIN_LEFT = 403

TOPBOX_TOP = 40
MIDBOX_TOP = 112
BOTTOMBOX_TOP = 361

BOX_LEFT = 42

FONT_COLOR = (255,255,255)

ROW_N = 12
COL_N = 10

FPS = 30
FPSCLOCK = pygame.time.Clock()

# define items
UPGRADE_PRICE = [0, 20, 100, 500, 1500, 3000, 5000, 8000, 13000, 21000, 36000, 55000]
POUCH = [1, 2, 5, 10, 15, 20, 25, 30, 35, 40, 50]
SWORD = [1, 2, 5, 7, 11, 13, 17, 21, 28, 31, 35]
SHIELD = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ARMOR = [1, 3, 5, 7, 9, 11, 13, 15, 17, 20]
ROD = [1, 2, 5, 7, 11, 13, 17, 21, 28, 31, 35]
LIFE = [100, 130, 160, 200, 240, 300, 360, 420, 500, 580, 660]
SLOW = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
HEALING_GEM = [1, 3, 5, 7, 11, 15, 20, 26, 33, 40, 55]
CRIT_GEM = [1, 3, 5, 7, 9, 10, 11, 12, 13, 14, 18]

# define enemies

ENEMY = [{"NAME":"Slime", "HP":8, "DMG":10, "ATK_SPD":15, "MAGIC_DMG":None, "MAGIC_SPD":None,"SPECIAL_DMG":None, "SPECIAL_COOLDOWN":None,"GOLD":8 },
         {"NAME":"Imp", "HP":25, "DMG":None, "ATK_SPD":None, "MAGIC_DMG":15, "MAGIC_SPD":16,"SPECIAL_DMG":45, "SPECIAL_COOLDOWN":30,"GOLD":15 },
         {"NAME":"Skeleton", "HP":40, "DMG":35, "ATK_SPD":18, "MAGIC_DMG":None, "MAGIC_SPD":None,"SPECIAL_DMG":55, "SPECIAL_COOLDOWN":36,"GOLD":30 },
         {"NAME":"Ogre", "HP":100, "DMG":40, "ATK_SPD":20, "MAGIC_DMG":None, "MAGIC_SPD":None,"SPECIAL_DMG":60, "SPECIAL_COOLDOWN":60,"GOLD":40 },
         {"NAME":"Ghost", "HP":110, "DMG":None, "ATK_SPD":None, "MAGIC_DMG":35, "MAGIC_SPD":9,"SPECIAL_DMG":70, "SPECIAL_COOLDOWN":30,"GOLD":50 },
         {"NAME":"Werewolf", "HP":190, "DMG":50, "ATK_SPD":20, "MAGIC_DMG":None, "MAGIC_SPD":None,"SPECIAL_DMG":70, "SPECIAL_COOLDOWN":45,"GOLD":80 },
         {"NAME":"Lizard", "HP":300, "DMG":70, "ATK_SPD":22, "MAGIC_DMG":20, "MAGIC_SPD":60,"SPECIAL_DMG":30, "SPECIAL_COOLDOWN":80,"GOLD":150 },
         {"NAME":"Oni", "HP":300, "DMG":90, "ATK_SPD":20, "MAGIC_DMG":None, "MAGIC_SPD":None,"SPECIAL_DMG":90, "SPECIAL_COOLDOWN":50,"GOLD":180 },
         {"NAME":"Demon", "HP":500, "DMG":110, "ATK_SPD":18, "MAGIC_DMG":70, "MAGIC_SPD":28,"SPECIAL_DMG":160, "SPECIAL_COOLDOWN":80,"GOLD":250 },
         {"NAME":"Dragon", "HP":800, "DMG":200, "ATK_SPD":20, "MAGIC_DMG":20, "MAGIC_SPD":30,"SPECIAL_DMG":250, "SPECIAL_COOLDOWN":70,"GOLD":500 }
         ]

ENEMY_NAMES = [row["NAME"] for row in ENEMY]
LEVELS = [[0],[0,0],[0,1],[1,1,2],[2,2,3],[3,3,4],[4,5],[4,5,5],[5,5],[5,1,2,6],[6,1,1,6],[7,4,3,1],[7,7,8],[8,8,9],[0,1,2,3,4,5,6,7,8,9]]
STAGE_NAME = ["The cave", "Deeper cave", "Swamp", "Crossroads", "Snow mountain",
              "Ice peak", "Rabbit hole", "Abandoned mines", "Deep pit",
              "Lava field", "Cemetery", "Chapel", "Crypt",
              "Idol room", "Treasure room"
              ]

# define constants for left part of screen
LVL_GFX = {"g":"green_dot","up_enable":"lvl_up_on","up_max":"lvl_up_max"}
DOTS_TOP = 375
DOTS_TOP_SPACING = 47
DOTS_LEFT = 91
DOTS_LEFT_SPACING = 20.4
PLUS_TOP = 369
PLUS_TOP_SPACING = 47
PLUS_LEFT = 304

