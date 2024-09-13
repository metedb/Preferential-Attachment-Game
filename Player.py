import pygame
pygame.init()
pygame.font.init()
from main import MovingObject, Bullet, WHITE


class Player(MovingObject):
    def __init__(self, color, damage, bullets_amount, speed, group, bullets_group, screen):
        super().__init__(color, speed, group, screen)
        self._bullets = bullets_amount
        self._bullets_group = bullets_group
        self._damage = damage

    def increase_bullet(self):
        self._bullets += 1
    
    def shoot(self, target_x, target_y):
        if self._bullets >= 1:
           x, y = self.rect.centerx, self.rect.centery
           bullet = Bullet(WHITE, 10, self._bullets_group, x, y, target_x, target_y, self._damage, self._screen)
           self._bullets -= 1

    def display_your_ammunition(self):
        font = pygame.font.Font(None, 48)
        text = font.render("Bullets: " + str(self._bullets), True, (255, 255, 255))
        text_width = text.get_width()
        self._screen.blit(text, (self._screen_width - 1.5 * text_width, 40))
        pygame.display.flip()

    def you_keep_moving(self, right, left, up, down):
        if right:
            self.move(1,0)
        if left:
            self.move(-1,0)
        if down:
            self.move(0, 1)
        if up:
            self.move(0, -1)

    def move(self, dx, dy):
        self._dx, self._dy = dx, dy
        super().move()