'''
Created on 14 feb 2021

'''

from settings import *
import json

class Player:
    def __init__(self):
        self.all_stats = self.load_inventory()
        self.hp = 100
        # temporary effects holding variables
        self.active_magic_def = self.magic_def
        self.current_hp = self.hp
        
        self.bonus_magic_def = 0
        self.bonus_magic_def_turns = 0
        
        self.bonus_shield_def = 0
        self.bonus_shield_def_turns = 0
        
        # and available golds
        self.gold = 0
    
    def level_up(self, level):
        self.hp += (level*100)//4
        self.current_hp += (level*100)//4
    
    def turn(self):
        # control active defense buffs
        
        if self.bonus_magic_def_turns > 0:
            self.bonus_magic_def_turns -= 1
            if self.bonus_magic_def_turns == 0:
                self.magic_def -= self.bonus_magic_def
                self.bonus_magic_def = 0
        
        if self.bonus_shield_def_turns > 0:
            self.bonus_shield_def_turns -= 1
            if self.bonus_shield_def_turns == 0:
                self.shield -= self.bonus_shield_def
                self.bonus_shield_def = 0
        
        
    def load_inventory(self):
        jfile = open("inventory.json", "r")
        self.save_stats = json.load(jfile)
        equipment = self.save_stats["equipment"]
        jfile.close()
        
        # set equipment
        self.sword_level = equipment["phys_atk"]
        self.shield_level = equipment["phys_def"]
        self.rod_level = equipment["magic_atk"]
        self.armor_level = equipment["magic_def"] 
        self.pouch_level = equipment["gold_bag"]
        self.slow_level = equipment["slow_amnt"]
        self.crit_level = equipment["crit_perc"]
        self.healing_level = equipment["heal_potion"]
        
        # create a new player and set base stats
        self.atk = SWORD[self.sword_level]
        self.shield = SHIELD[self.shield_level]
        self.magic_def = ARMOR[self.armor_level]
        self.magic_atk = ROD[self.rod_level]
        self.magic_slow = SLOW[self.slow_level]
        self.crit = CRIT_GEM[self.crit_level]
        self.healing = HEALING_GEM[self.healing_level]
        self.pouch_amount = POUCH[self.pouch_level]
        
        self.bonus_crit = 0
        
        all_stats = [self.pouch_level, self.sword_level, self.shield_level,
                     self.healing_level, self.armor_level, self.rod_level,
                     self.slow_level, self.crit_level] 
        
        return all_stats
    
    def upgrade_item(self, item):
        self.all_stats[item]+=1
        self.gold -= UPGRADE_PRICE[self.all_stats[item]]
        json_data = {"equipment": {
            "gold_bag":self.all_stats[0],
            "phys_atk":self.all_stats[1],
            "phys_def":self.all_stats[2],
            "heal_potion":self.all_stats[3],
            "magic_def":self.all_stats[4],
            "magic_atk":self.all_stats[5],
            "slow_amnt":self.all_stats[6],
            "crit_perc":self.all_stats[7]
            }
        }
        
        with open("inventory.json", "w") as json_file:
            json.dump(json_data, json_file)
        self.load_inventory()
    
    def heal(self, amount):
        new_hp = self.current_hp + (amount*self.healing)
        self.current_hp = min(new_hp, self.hp)
    
    def magic_def_up(self, amount):
        self.bonus_magic_def = amount
        self.bonus_magic_def_turns = amount
        self.active_magic_def += self.bonus_magic_def
    
    def shield_def_up(self, amount):
        self.bonus_shield_def = amount
        self.bonus_shield_def_turns = amount
        self.shield += self.bonus_shield_def
    
    def add_gold(self, amount):
        self.gold += POUCH[self.pouch_amount]*amount
    
    def calc_magic_damage(self, amount):
        return self.magic_atk * amount
    
    def calc_weapon_damage(self, amount):
        return (self.atk * amount)+((self.atk * amount)*(self.crit//100))
    
    def next_crit(self, amount):
        self.crit+=amount
        self.bonus_crit=amount
        
    def remove_crit(self):
        self.crit -= self.bonus_crit
        self.bonus_crit = 0
    
    def get_damage(self, damage):
        total_damage = 0
        
        # Physical damage calculation with gear and perks reduction
        if damage["weapon"] > 0:
            weapon_dmg = damage["weapon"]-(self.shield+SHIELD[self.shield_level]+ARMOR[self.armor_level])
            total_damage += weapon_dmg
            
        # Magic damage calculation with gear and perks reduction
        if damage["magic"] > 0:
            magic_dmg = damage["magic"]-self.active_magic_def
            total_damage += magic_dmg
            
        # Special damage, hit phys or magic, the one with less defence
        if damage["special"] > 0:
            physical = damage["special"]-(self.shield+SHIELD[self.shield_level]+ARMOR[self.armor_level])
            magic = damage["special"]-self.active_magic_def
            special_dmg = max(physical, magic)
            total_damage += special_dmg
            
        if total_damage > 0:
            self.current_hp -= total_damage 
                
        if self.current_hp <= 0:
            return "DEAD"
        else:
            return "ALIVE"
    
class Enemy:
    def __init__(self, level, img):
        self.hp = ENEMY[level]["HP"]
        self.dmg = ENEMY[level]["DMG"]
        self.gold = ENEMY[level]["GOLD"]
        self.name = ENEMY[level]["NAME"]
        self.atk_speed = ENEMY[level]["ATK_SPD"]
        self.magic_dmg = ENEMY[level]["MAGIC_DMG"]
        self.magic_speed = ENEMY[level]["MAGIC_SPD"]
        self.special_dmg = ENEMY[level]["SPECIAL_DMG"]
        self.special_speed = ENEMY[level]["SPECIAL_COOLDOWN"]
        
        self.img = img
        
        self.global_cooldown = 0
        
        self.atk_cooldown = self.atk_speed
        self.magic_cooldown = self.magic_speed
        self.special_cooldown = self.special_speed
        
        self.active_enemy = False
        
    def apply_damage(self, damage):
        self.hp -= damage
        
        if self.hp <= 0:
            message = f"You kill a {self.name}!"
            return message
        
        return -1
    
    def slowdown(self, amount):
        if self.atk_cooldown != None:
            self.atk_cooldown += amount
        
        if self.magic_cooldown != None:
            self.magic_cooldown = amount
        
        if self.special_speed != None:
            self.special_cooldown += amount  
        
    def turn(self):
        damage = {"weapon":0, "magic":0, "special":0} 
        self.global_cooldown+=1
        if self.global_cooldown == 30:
        
            if self.dmg != None:
                self.atk_cooldown-=1
                if self.atk_cooldown == 0:
                    damage["weapon"] = self.dmg
                    self.atk_cooldown = self.atk_speed 
            
            if self.magic_dmg != None:
                self.magic_cooldown -= 1
                if self.magic_cooldown == 0:
                    damage["magic"] = self.magic_dmg
                    self.magic_cooldown = self.magic_speed
            
            if self.special_dmg != None:
                self.special_cooldown -= 1
                if self.special_cooldown == 0:
                    damage["special"] = self.special_dmg
                    self.special_cooldown = self.special_speed
            
            self.global_cooldown = 0
        
        return damage
        