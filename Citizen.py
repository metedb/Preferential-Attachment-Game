from main import Sprite, Militant, RED



class Citizen(Sprite):
    def __init__(self, color, radius, group, screen):
        super().__init__(color, radius, group, screen)

    def turn_to_militant(self, militia_group):
        new_militant = Militant(RED, 1, militia_group, self._screen, self.rect.centerx, self.rect.centery)
        return new_militant