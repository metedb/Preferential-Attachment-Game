from main import SpriteGroup

import numpy as np




class Militia(SpriteGroup):
    def __init__(self, all_sprites_group):
        super().__init__(all_sprites_group)
        self._ranks = {}

    def here_is_my_rank(self, sprite, rank):
        self._ranks[sprite] = rank
            
 
    def diffusion(self):
        for militant in self._sprites:
            militant.diffuse_down()
        
    def recruit(self, new_militant, links):  
        mentor = self.find_mentor()
        mentor.add_link(new_militant, links)

    def find_mentor(self):
        total_rank = sum(rank for rank in self._ranks.values()) 
        probs = [rank / total_rank for rank in self._ranks.values()]
        keys = list(self._sprites)
        mentor = np.random.choice(keys, p = probs)
        return mentor
    
    def update_radius_and_color(self):
        for militant in self._sprites:
            militant.update_radius_and_color()

    def update_my_rank(self, mentor, new_rank):
        self._ranks[mentor] = new_rank

    def who_is_your_biggest_mentor(self, caller):
        biggest_mentor = max(self._ranks, key = self._ranks.get)
        biggest_mentor.be_chased_by(caller)
   

    def initialize_militants(self, links_group):
      for i, militant_i in enumerate(list(self._sprites)):
            for j in list(self._sprites)[i+1:]:
                  militant_i.add_link(j, links_group)