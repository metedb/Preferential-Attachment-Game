import pygame
pygame.init()
pygame.font.init()
from main import Player



class CPU_Player(Player):
    def __init__(self, color, damage, ammo_amount, speed, group, bullets_group, militia_group, screen):
        super().__init__(color, damage, ammo_amount, speed, group, bullets_group, screen)
        self._shooting_freq = 200
        self._last_shot = 0
        self._militia_group = militia_group

    def check_shooting_distance(self):
        self._distance_to_tar = pygame.math.Vector2(self._target_x - self.rect.centerx, self._target_y - self.rect.centery).length()
        if self._distance_to_tar <= self._shooting_freq: self._stop = True
        else: self._stop = False

    def stop_and_shoot(self):
        current_time = pygame.time.get_ticks()
        time_since_last_shot = current_time - self._last_shot
        if time_since_last_shot >= 1000:
            self._last_shot = current_time
            self.shoot(self._target_x,self._target_y)

    def set_direction(self, target_x, target_y):
        self._target_x = target_x
        self._target_y = target_y
        super().set_direction(self._target_x, self._target_y)

    def doctrinate_your_militants(self):
        self._militia_group.who_is_your_biggest_mentor(self)
        self.check_shooting_distance()
        if self._stop == True:
          self.stop_and_shoot()
          self._militia_group.who_is_your_biggest_mentor(self)
        else: self.move(self._dx, self._dy)