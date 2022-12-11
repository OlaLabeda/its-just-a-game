from random import randint 


class NegativeLivesError(Exception): # dziedziczy po jakims istniejacym wyjatku
    def __init__(self, lives):
        super().__init__('Lives cannot be negative')
        self.lives = lives
 
class NameError(Exception):
    pass


class NegativeHealthError(Exception):
    def __init__(self, health):
        super().__init__('Health cannot be negative')
        self.health = health
        

class NegativeDamageError(Exception):
    def __init__(self, damage):
        super().__init__('Damage cannot be negative')
        self.damage = damage
        

class NotEnoughHeadsError(Exception):
    def __init__(self, heads):
        super().__init__('Hydra needs to have at least one head')
        self.heads = heads


class NegativePointsNumberError(Exception):
    def __init__(self, points):
        super().__init__('Cannot regenerate negative number of points')
        self.points = points
    
    
class Player:
    """
    Class Player contains attributes:
    :param name: player's name
    :type name: str
    
    :param lives: player's lives, defaults to 1
    :type name: int
    
    """
    def __init__(self, name, lives = 1):
        self._name = name
        lives = int(lives)
        if lives < 0:
            raise NegativeLivesError(lives)
        self._lives = int(lives)
    
    
    def name(self):
        return self._name
        
    
    def set_name(self, new_name):
        if not new_name:
            raise NameError('Name cannot be empty')
        self._name = str(new_name).title()
        
    
    def lives(self):
        return self._lives
    
    
    def set_lives(self, new_lives):
        if new_lives < 0:
            raise NegativeLivesError(new_lives)
        self._lives = new_lives      
        
         
    def info(self):
        """
        Returns basic description of the player
        
        """
        if self._lives == 1:
            lives = 'life'
        else:
            lives = 'lives'
        return f'My name is {self._name}. I have {self._lives} {lives} left'
     
             
    def __str__(self):
        return self.info()


class Enemy:
    
    """
    Creates instance of enemy
    
    Raises error if name is empty or health drops below 0
    """
    def __init__(self, name, health):
        health = int(health)
        if health < 0:
            raise NegativeHealthError(health)
        if not name:
            raise NameError('Name cannot be empty')
        self._name = name
        self._health = int(health)
    
    
    def name(self):
        """

        Returns name of enemy
            
        """
        return self._name
    
    
    def set_name(self, new_name):
        """
        
        sets name of enemy
        
        """
        if not new_name:
            raise NameError('Name cannot be empty')
        self._name = new_name
    
    
    def health(self):
        """
        returns health of enemy
        
        """
        return self._health
    
    
    def set_health(self, new_health):
        """
        
        sets health of enemy
        
        """
        self._health = max(new_health, 0)
    

    def __str__(self):
        return f'This is {self._name}. It has {self._health} points left'
    
    
    def take_damage(self, damage):
        """ 
        
        drops health of enemy
        
        """
        if damage <= 0:
            raise NegativeDamageError(damage)
        self._health -= min(self._health, damage)
        
    
    def is_alive(self):
        """
        
        returns true if health is greater than 0
        
        """
        return self._health > 0
    
 
class Hydra(Enemy):
    
    """
    
    Creates Instance of Hydra
    
    """
    def __init__(self, name, health, heads=1):
        super().__init__(name, health)
        if heads < 1:
            raise NotEnoughHeadsError(heads)
        self._heads = heads
        self._base_health = health
    
    
    def heads(self):
        return self._heads
    
    
    def base_health(self):
        return self._base_health
    
    
    def regenerate(self, points):
        if points < 0:
            raise NegativePointsNumberError(points)
        if self._health >= self._base_health:
            return
        self._health = min(points + self._health, self._base_health)
        
        
    def __str__(self):
        base = super().__str__()
        return f'{base} and {self._heads} heads'
    

class DragonHydra(Hydra):
    def take_damage(self, damage):
        if randint(0, 1):
            super().take_damage(damage)
            
            
class Game:
    def __init__(self, player, enemies = None):
        self.player = player
        self.enemies = enemies if enemies else []
        # niezmiennik - nie hcce ryzykowac ze ktos mi cos rozgrzebie
        self._result = None
        
        