import pygame
pygame.init()
pygame.font.init()
import random
from main import MovingObject, Link



class Militant(MovingObject):
    def __init__(self, color, speed, group, screen,x = None, y = None):
        super().__init__(color, speed, group, screen, x = x, y = y)
        self._mentees = []
        self._rank = 1
        self._ideology = 20
        self._group.here_is_my_rank(self,self._rank)



    def add_link(self, mentee, links_group):
        link = Link(self, mentee, links_group, self._screen)
        self._mentees.append(mentee)
        self._rank += 1
        self._group.update_my_rank(self, self._rank)



    def update_radius_and_color(self):
        self._radius = self._rank * 5
        self.image = pygame.Surface([self._radius*2, self._radius*2], pygame.SRCALPHA)
        if self._ideology >= 0:
           self._color = (255, 255 - 12.5 * self._ideology, 255 - 12.5 * self._ideology)
        else: self._color = (255 + 12.5 * self._ideology, 255 + 12.5 * self._ideology, 255)
        pygame.draw.circle(self.image, self._color, (self._radius, self._radius), self._radius)

    def diffuse_down(self):
        for mentee in self._mentees:
            mentee.get_diffused(self._ideology)

    def get_hit(self, damage):
        if damage >= 0:
          if self._ideology >= -18:
            self._ideology -= damage
          else:
            self._ideology = -20
        else:
            if self._ideology <= 18:
              self._ideology -= damage
            else:
              self._ideology = 20

    def get_diffused(self, mentor_ideology):
        self._ideology = 0.2 * self._ideology + 0.8 * mentor_ideology


    def are_you_communist(self):
        if self._ideology > 0:
            return True

    def move(self):
        self._dx, self._dy = random.randint(-5,5), random.randint(-5,5)
        super().move()
