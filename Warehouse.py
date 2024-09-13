import pygame
pygame.init()
pygame.font.init()
from main import Sprite, PURPLE, WHITE





class Warehouse(Sprite):
    def __init__(self, color, radius, group, screen, my_shape = "square"):
        super().__init__(color, radius, group, screen, shape = my_shape)
        self._current_wait_length = None
        self._flag = None
        
    
    
    def supply(self, player):
        self.image.fill(PURPLE)
        current_time = pygame.time.get_ticks()

        if(self._flag == 0):
            self._last_time = pygame.time.get_ticks()

        difference = current_time - self._last_time
        self._current_wait_length += difference

        if self._current_wait_length >= 100:
            player.increase_bullet()
            self._current_wait_length = 0

        self._last_time = pygame.time.get_ticks()
        self._flag += 1


    def reset_stats(self):
        self._flag = 0
        self._current_wait_length = 0
        self._last_time = None
        self.image.fill(WHITE)