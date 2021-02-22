'''
Created on 15 feb 2021
'''
def calculate_score(gems, player, enemy):
    ''' gems contain a dictionary with pair {"color":n}
    "g", "b", "r", "p", "y", "v", "o", "c"
    
    g -> gold
    b -> attack
    r -> shield
    p -> heal
    y -> magic defence
    v -> magic damage
    o -> magic slow
    c -> crit %
    '''
    
    damage = 0
    
    if gems["g"] > 0:
        if sum(player.all_stats)==10*len(player.all_stats):
            damage =player.calc_weapon_damage(gems["g"])
        else:
            player.add_gold(gems["g"])
    
    if gems["r"] > 0:
        player.shield_def_up(gems["r"])
    
    if gems["p"] > 0:
        player.heal(gems["p"])
    
    if gems["y"] > 0:
        player.magic_def_up(gems["y"])

    if gems["o"] > 0:
        enemy.slowdown(player.magic_slow * gems["o"])
    
    if gems["c"] > 0:
        player.next_crit(gems["c"])
        
    if gems["v"] > 0:
        damage = player.calc_magic_damage(gems["v"]) 
        
    if gems["b"] > 0:
        damage += player.calc_weapon_damage(gems["b"])
        player.remove_crit()
        
    if damage > 0:
        return enemy.apply_damage(damage)
    else:
        return -1