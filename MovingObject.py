import pygame
pygame.init()
pygame.font.init()
from main import Sprite



class MovingObject(Sprite):
  
  def __init__(self, color, speed, group, screen, radius = 10, x = None, y = None):
      super().__init__(color, radius, group, screen, x = x, y = y)
      self._speed = speed
      self._dx = None
      self._dy = None

  def move(self):
       
       self.rect.centerx += self._speed * self._dx
       self.rect.centery += self._speed * self._dy   
       self.check_boundaries() 

  def check_boundaries(self):
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.rect.x += self._speed * - self._dx
      
        if self.rect.right > self._screen_width:
            self.rect.right = self._screen_width
            self.rect.x += self._speed * - self._dx
      
        if self.rect.top < 0:
            self.rect.top = 0
            self.rect.y += self._speed * - self._dy
      
        if self.rect.bottom > self._screen_height:
            self.rect.bottom = self._screen_height
            self.rect.y += self._speed * - self._dy

  def be_chased_by(self, caller):
      caller.set_direction(self.rect.centerx, self.rect.centery)

  def set_direction(self, target_x, target_y):
        direction = pygame.math.Vector2(target_x - self.rect.centerx, target_y - self.rect.centery)
        direction.normalize_ip()
        self._dx, self._dy = direction.x, direction.y