import pygame
import random
pygame.init()
pygame.font.init()



class Sprite():
    def __init__(self, color, radius, group, screen, x = None, y = None, shape = "circle"):
        self._screen = screen
        self._screen_height = self._screen.get_height()
        self._screen_width = self._screen.get_width()

        if x == None:
            x = random.randint(0, self._screen_width - 20)

        if y == None:
            y = random.randint(0, self._screen_height - 20)

        self._color = color
        self._radius = radius
        self._group = group
        self._group.add(self)

        if shape == "circle":
          self.image = pygame.Surface([self._radius*2, self._radius*2], pygame.SRCALPHA)
          pygame.draw.circle(self.image, self._color, (self._radius, self._radius), self._radius)
          self.rect = self.image.get_rect()
          self.rect.centerx = x
          self.rect.centery = y

        if shape == "square":
            self.image = pygame.Surface((self._radius, self._radius))
            pygame.draw.rect(self.image, self._color, [0, 0, self._radius, self._radius])
            self.rect = self.image.get_rect()
            self.rect.centerx = self._screen_width / 2
            self.rect.centery = self._screen_height - self._radius
       
        self.rect.centerx = x
        self.rect.centery = y

    
    def check_your_individual_collision_with(self,other_sprite):
        my_pos = pygame.math.Vector2(self.rect.center)
        return other_sprite.did_we_collide(my_pos, self._radius)
  
    def did_we_collide(self, other_sprite_pos, other_sprite_rad):
        my_pos = pygame.math.Vector2(self.rect.center)
        if my_pos.distance_to(other_sprite_pos) <= self._radius + other_sprite_rad:
            return True
        

    def draw(self):
        self._screen.blit(self.image, self.rect)

    def remove(self):
        self._group.remove_me(self)