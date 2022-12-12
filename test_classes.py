from classes import Player, Enemy, Hydra, DragonHydra, Game
from classes import (
        NegativePowerError,
        NameError, NegativeHealthError,
        NegativeDamageError, 
        NotEnoughHeadsError,
        NegativePointsNumberError
)

import pytest

def test_create_player():
    player = Player('Jurek Ogorek')
    assert player.name() == 'Jurek Ogorek'
    assert player.power() == 5
    

def test_create_player_with_power():
    player = Player('Jurek Ogorek', 4)
    assert player.name() == 'Jurek Ogorek'
    assert player.power() == 4

         
def test_create_player_with_negative_power():
    with pytest.raises(NegativePowerError):
        player = Player('Jurek Ogorek', -6)


def test_introduce():
    player = Player('Jurek Ogorek', 3)
    assert player.info() == 'My name is Jurek Ogorek. I have 3 power left'
    
    
def test_introduce_as_str():
    player = Player('Jurek Ogorek', 3)
    assert str(player) == player.info()
    player = Player('Jurek Ogorek', 1)
    assert str(player) == player.info()
    
    
def test_set_name():
    player = Player('Jurek Ogorek')
    assert player.name() == 'Jurek Ogorek'
    

def test_set_name_empty():
    player = Player('Jurek Ogorek')
    with pytest.raises(NameError):
        player.set_name('')
        
        
def test_set_name_lowercase():
    player = Player('Jurek Ogorek')
    assert player.name() == 'Jurek Ogorek'
    player.set_name('karolina malina')
    assert player.name() == 'Karolina Malina'
    

def test_set_power():
    player = Player('Jurek Ogorek', 1)
    assert player.power() == 1
    player.set_power(2)
    assert player.power() == 2


def test_set_power_zero():
    player = Player('Jurek Ogorek', 1)
    assert player.power() == 1
    player.set_power(0)
    assert player.power() == 0
    
    
def test_set_power_negative():
    player = Player('Jurek Ogorek', 1)
    assert player.power() == 1
    with pytest.raises(NegativePowerError):
        player.set_power(-1)
    

def test_attack():
    player = Player('Jurek Ogorek')
    assert player.power() == 5
    orc = Enemy('orc', 10)
    assert orc.health() == 10
    enemies = [orc]
    target, damage, status = player.attack(enemies)
    assert target == orc
    assert status is True
    assert player.power() == 4
    assert orc.health() < 10
    assert orc.health() == 10 - damage
    
    
def test_attack_choice():
    player = Player('Jurek Ogorek')
    orc1 = Enemy('orc1', 10)
    orc2 = Enemy('orc2', 20)
    base_health = {orc1: 10, orc2: 20}
    enemies = [orc1, orc2]
    target, damage, status = player.attack(enemies)
    assert status is True
    assert player.power() == 4
    assert target in enemies
    assert target.health() < base_health[target]
    assert target.health() == base_health[target] - damage
    # assert orc1.health() < 10 or orc2.health() < 20
        
        
def test_attack_choose_enemy(monkeypatch):
    player = Player('Jurek Ogorek')
    orc1 = Enemy('orc1', 10)
    orc2 = Enemy('orc2', 20)
    enemies = [orc1, orc2]  

    def get_orc2(orcs):
        return orc2
    monkeypatch.setattr('classes.choice', get_orc2)
    target, damage, status = player.attack(enemies)    
    assert status is True
    assert target == orc2
    assert player.power() == 4
    assert orc1.health() == 10 and orc2.health() == 20 - damage 
      
      
def test_attack_no_power():
    player = Player('Jurek Ogorek', 0)
    assert player.power() == 0
    orc = Enemy('orc', 10)
    assert orc.health() == 10
    enemies = [orc]
    target, damage, status = player.attack(enemies)
    assert status is False
    assert damage == 0
    assert target is None
    assert player.power() == 0
    assert orc.health() == 10
    
    
def test_attack_power_eq_1():
    player = Player('Jurek Ogorek', 1)
    assert player.power() == 1
    orc = Enemy('orc', 10)
    assert orc.health() == 10
    enemies = [orc]
    target, damage, status = player.attack(enemies)
    player.attack(enemies)
    assert damage == 1
    assert target == orc
    assert status is True
    assert player.power() == 0
    assert orc.health() == 9
     
def test_attack_power(monkeypatch):
    player = Player('Jurek Ogorek')
    assert player.power() == 5
    orc = Enemy('orc', 10)
    assert orc.health() == 10
    enemies = [orc]

    def damage_two(t, f):
        return 2
    monkeypatch.setattr('classes.randint', damage_two)
    target, damage, status = player.attack(enemies)
    assert target == orc
    assert damage ==2
    assert status is True
    assert player.power() == 4
    assert orc.health() == 8


def test_attack_set_power():
    player = Player('Jurek Ogorek')
    assert player.power() == 5
    player.set_power(10)
    assert player.power() == 10
    

def test_attack_set_power_negative():
    player = Player('Jurek Ogorek')
    assert player.power() == 5
    player.set_power(10)
    assert player.power() == 10
         
     
def test_enemy_create():
    enemy = Enemy('orc', 50)
    assert enemy.name() == 'orc'
    assert enemy.health() == 50
        
        
def test_enemy_with_negative_health():
    with pytest.raises(NegativeHealthError):
        Enemy('orc', -10)
        
        
def test_create_enemy_with_empty_name():
    with pytest.raises(NameError):
        Enemy('', 5)
        
        
def test_enemy_set_name():
    enemy = Enemy('orc', 50)
    assert enemy.name() == 'orc'
    enemy.set_name('dragon')
    assert enemy.name() == 'dragon'
    
    
def test_enemy_set_empty_name():
    enemy = Enemy('orc', 50)
    with pytest.raises(NameError):
        enemy.set_name('')
        
        
def test_enemy_set_health():
    enemy = Enemy('orc', 50)
    assert enemy.health() == 50
    enemy.set_health(-10)
    assert enemy.health() == 0
    
    
def test_enemy_description():
    enemy = Enemy('orc', 40)
    assert str(enemy) == 'This is orc. It has 40 points left'
    
    
def test_enemy_take_damage():
    enemy = Enemy('orc', 50)
    assert enemy.health() == 50
    assert enemy.take_damage(10) is True
    assert enemy.health() == 40
    

def test_take_damage_invalid():
    # nie musze robic asercji bo jezeli chce 
    # odjac ujemna liczbe zycia to to bullshit
    enemy = Enemy('orc', 50)
    with pytest.raises(NegativeDamageError):
        enemy.take_damage(-10)
    with pytest.raises(NegativeDamageError):
        enemy.take_damage(0)
        

def test_take_damage_drops_below_zero():
    enemy = Enemy('orc', 10)
    # skoro uzywam teg
    assert enemy.health() == 10
    assert enemy.take_damage(30) is True
    assert enemy.health() == 0


def test_enemy_is_alive():
    enemy = Enemy('orc', 10)
    assert enemy.health() == 10
    assert enemy.is_alive() 
    

def test_enemy_is_alive_false():
    enemy = Enemy('orc', 0)
    assert enemy.health() == 0
    assert not enemy.is_alive()
    

def test_hydra_create():
    hydra = Hydra('Hydra', health = 20, heads = 3)
    assert hydra.name() == 'Hydra'
    assert hydra.health() == 20
    assert hydra.heads() == 3
    
    
def test_hydra_heads():
    hydra = Hydra('Hydra', 5, 4)
    assert hydra.name() == 'Hydra'
    assert hydra.health() == 5
    assert hydra.heads() == 4
    

def test_hydra_create_default_heads():
    hydra = Hydra('Hydra', health = 5)
    assert hydra.name() == 'Hydra'
    assert hydra.health() == 5
    assert hydra.heads() == 1
    
    
def test_hydra_description():
    hydra = Hydra('green hydra', 5, 3)
    assert str(hydra) == 'This is green hydra. It has 5 points left and 3 heads'
    
    
def test_hydra_regenerate():
    hydra = Hydra('green hydra', 30, 3)
    hydra.take_damage(10)
    hydra.regenerate(5)
    assert hydra.health() == 25
    
    
def test_hydra_regenerate_max_health():
    hydra = Hydra('green hydra', 30, 3)
    hydra.take_damage(10)
    hydra.regenerate(15)
    assert hydra.health() == 30
    

def test_hydra_base_health():
    hydra = Hydra('two headed hydra', 30, 2)
    assert hydra.base_health() == 30


def test_hydra_set_health_above_base():
    hydra = Hydra('two headed hydra', 30, 2)
    assert hydra.base_health() == 30
    hydra.set_health(50)
    assert hydra.health() == 50
    assert hydra.base_health() == 30
    
    
def test_hydra_regenerate_health_above_base():
    hydra = Hydra('two headed hydra', 30, 2)
    assert hydra.base_health() == 30
    hydra.set_health(50)
    hydra.take_damage(10)
    hydra.regenerate(5)
    assert hydra.health() == 40
    
# testy musza byc deterministyczne - za kazdym razem
# daja ten sam wynik jezeli testuja to samo
def test_dragonhydra_take_damage_hit(monkeypatch):
    def returnOne(f, t):
        return 1
    monkeypatch.setattr('classes.randint', returnOne)
    enemy = DragonHydra('dragon', 40, 3)
    assert enemy.health() == 40
    assert enemy.take_damage(10) is True
    assert enemy.health() == 30
    
    
def test_dragonhydra_take_damage_nohit(monkeypatch):
    def returnZero(f, t):
        return 0
    monkeypatch.setattr('classes.randint', returnZero)
    enemy = DragonHydra('dragon', 40, 3)
    assert enemy.health() == 40
    assert enemy.take_damage(10) is False
    assert enemy.health() == 40
    
    
def test_game_create():
    player  = Player('Jurek Ogorek')
    enemies = [
        Hydra('hydra', 10, 1),
        Enemy('orc', 20)
    ]
    game = Game(player, enemies)
    assert game.player == player
    assert game.enemies == enemies
    
def test_game_create_default_enemies():
    player = Player('Jurek Ogorek')
    game = Game(player)
    assert game.player == player
    assert game.enemies == []
    
    