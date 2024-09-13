from main import MovingObject

class Bullet(MovingObject):
    def __init__(self, color, speed, group, x, y, target_x, target_y, damage, screen, radius = 4):
        super().__init__(color, speed, group, screen, radius, x = x, y = y)
        self._damage = damage
        self.set_direction(target_x, target_y)

    def hit_militant(self, damaged_militant):
        damaged_militant.get_hit(self._damage)
        self.remove()

    def move(self):
        self.rect.centerx += self._speed * self._dx
        self.rect.centery += self._speed * self._dy 