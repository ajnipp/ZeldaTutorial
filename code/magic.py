import pygame
from settings import *
from random import randint
class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player = animation_player

    def heal(self,player,strength,cost,groups):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura',player.rect.center,groups)
            self.animation_player.create_particles('heal',player.rect.center + pygame.math.Vector2(0,-60),groups)


    def flame(self,player,cost,groups):
        if player.energy >= cost:
            player.energy -= cost

            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0,-1)
            else: direction = pygame.math.Vector2(0, 1)

            for i in range(1,6):
                offset = (direction * i) * TILESIZE
                random_offset_value = randint(-TILESIZE // 3, TILESIZE // 3)
                random_offset = pygame.math.Vector2(random_offset_value, random_offset_value)
                magicPos = player.rect.center + offset + random_offset
                x = magicPos.x
                y = magicPos.y
                self.animation_player.create_particles('flame',(x,y),groups)




