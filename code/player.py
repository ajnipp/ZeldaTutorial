import pygame
from settings import *
from support import *
from debug import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        """
        Populates self.animations dictionary with animations from the player graphics folder.
        Uses the import_folder method to generate pygame surfaces for each frame and add them to
        the appropriate list in the dictionary.
        """
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [],
                           'right': [], 'right_idle': [], 'left_idle': [],
                           'down_idle': [], 'up_idle': [], 'right_attack': [],
                           'left_attack': [], 'up_attack': [], 'down_attack': []
                           }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        """
        Updates the status of the player according to its previous status and current movement.
        """
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    # overwrite idle
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def input(self):
        """
        Collect user input and update Player status and direction as needed. No updates to player state
        will be made if the player is attacking.
        """
        keys = pygame.key.get_pressed()
        if not self.attacking:
            # Vertical input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # Horizontal input
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')

    def move(self, speed):
        """
        Updates player position. Moves hitbox first, checks for collisions, then moves player to
        position of hitbox.
        :param speed: magnitude of velocity
        """
        if self.direction.magnitude() != 0:  # vector of 0 cannot be normalized
            self.direction = self.direction.normalize()  # prevents diagonal movement from being faster
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center  # rect follows the hitbox

    def collision(self, direction):
        """
        Checks the hitbox of the player with the hitbox of all obstacle sprites. Uses the current player
        direction to determine whether the collision is horizontal or vertical. Resets hitboxes
        if there is a collision.
        :param direction: the direction the current player movement. Either 'horizontal' or 'vertical'
        """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def cooldowns(self):
        """
        Updates the player attacking property. If the attack_cooldown has elapsed since the time of the
        first attack, then self.attacking is set to False.
        """
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        """
        Sets the current image according to the current status and animation frame
        """
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        debug(self.status)
