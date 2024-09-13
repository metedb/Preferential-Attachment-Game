from main import BaseGroup



class SpriteGroup(BaseGroup):
    def __init__(self, all_sprites):
        super().__init__()
        self._all_sprites = all_sprites

    def add(self, sprite):
        super().add(sprite)
        self._all_sprites.add(sprite)

    def check_collisions_with_my_sprites(self, other_group_sprites):   
       collisions = {}
       for sprite1 in self._sprites:
        for sprite2 in other_group_sprites:  
            if sprite1.check_your_individual_collision_with(sprite2):
                if sprite1 in collisions:
                    collisions[sprite1].append(sprite2)
                else:
                    collisions[sprite1] = [sprite2]
       return collisions
    
    def did_your_group_collide_with(self, other_group):
        if other_group.__class__.__name__ == "Player":
          return self.check_collisions_with_my_sprites({other_group})
        return other_group.check_collisions_with_my_sprites(self._sprites)

    def remove_me(self,sprite):
        if sprite in self._sprites:
          super().remove(sprite)
          self._all_sprites.remove(sprite)
        else:("Sprite not found in group", "\n")

    def hunt_down(self, player):
        for assassin in self._sprites:
            player.be_chased_by(assassin)
            assassin.move()

    def move(self):
        for sprite in self._sprites:
            sprite.move()