import pygame
pygame.init()
pygame.font.init()
from main import Sprite, WHITE


class Link(Sprite):
  def __init__(self, from_, to_, group, screen):
      super().__init__(WHITE, 1, group, screen)
      self._from = from_
      self._to = to_
  def draw(self):
    pygame.draw.aaline(self._screen, (255,255,255,0), self._from.rect.center, self._to.rect.center, blend = True)