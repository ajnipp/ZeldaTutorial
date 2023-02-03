import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()



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