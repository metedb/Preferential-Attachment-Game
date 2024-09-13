class BaseGroup():
   def __init__(self):
       self._sprites = set()

   def add(self, sprite):
       self._sprites.add(sprite)

   def draw(self):
        for sprite in self._sprites:
            sprite.draw()

   def remove(self, sprite):
         self._sprites.remove(sprite)