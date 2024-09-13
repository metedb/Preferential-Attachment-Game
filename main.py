import pygame
import random
import numpy as np

pygame.init()
pygame.font.init()



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
        list(self._sprites)[0].add_link(list(self._sprites)[1], links_group)






BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
PURPLE = (240,0,255)
BROWN = (102, 51, 0)






class Game:
  def __init__(self, militant_no, citizen_no, assassin_no, diffusion_freq, FPS = 60):
      self._MILITANT_NUMBER = militant_no
      self._ASSASSIN_NUMBER = assassin_no
      self._CITIZEN_NUMBER = citizen_no
      self._diffusion_freq = diffusion_freq
      self._FPS = FPS
      self._clock = pygame.time.Clock()
      self._running = None
      self._moving_right = None
      self._moving_left = None
      self._moving_up = None
      self._moving_down = None
      self._game_start = None
      self._game_paused = None
      self._last_diffusion = 0
      self._screen_width = 1400
      self._screen_height = 750
      self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.SRCALPHA)
      self.create_sprites_and_groups()




  
  
  def create_sprites_and_groups(self):
      self._all_sprites_group = BaseGroup()
      self._militia_group = Militia(self._all_sprites_group)
      self._bullets_group = SpriteGroup(self._all_sprites_group)
      self._citizens_group = SpriteGroup(self._all_sprites_group)
      self._assassins_group = SpriteGroup(self._all_sprites_group)
      self._links_group = SpriteGroup(self._all_sprites_group)
      
      warehouse = Warehouse(WHITE, 100, self._all_sprites_group, self._screen)
      self._warehouse = warehouse
      player = Player(WHITE, 3.5, 25, 6, self._all_sprites_group, self._bullets_group, self._screen)
      self._player = player
      cpu_player = CPU_Player(BROWN, -2,float('inf'), 5, self._all_sprites_group, self._bullets_group, self._militia_group, self._screen)
      self._cpu_player = cpu_player



      
      for i in range (self._MILITANT_NUMBER):
            militant = Militant(RED, 1, self._militia_group, self._screen)

      for i in range (self._CITIZEN_NUMBER):
            citizen = Citizen(WHITE, 3, self._citizens_group, self._screen)

      for i in range(self._ASSASSIN_NUMBER):
            assassin = MovingObject(BROWN, 3, self._assassins_group, self._screen)


      self._militia_group.initialize_militants(self._links_group)      
  

  def run(self):
      self._game_start == False
      self.start_screen()

  def start_screen(self):
      font = pygame.font.Font(None, 72)  
      text = font.render("START", True, (255, 255, 255))  
      text_rect = text.get_rect()
      BUTTON_WIDTH, BUTTON_HEIGHT = text_rect.width + 60, text_rect.height + 60 
      button = pygame.Rect((self._screen_width - BUTTON_WIDTH) // 2, (self._screen_height - BUTTON_HEIGHT) // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
      text_rect.center = button.center
      while not self._game_start:
          for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button.collidepoint(event.pos):
                        self._screen.fill(BLACK)
                        self._game_start = True
          self._screen.fill((255, 255, 255))  
          pygame.draw.rect(self._screen, (39, 58, 152), button)  
          self._screen.blit(text,text_rect)
          pygame.display.flip()  
      self.run_gameplay(self._FPS)

  def run_gameplay(self, FPS):
      self._running = True
      self._game_paused = False
      while self._running:
        self.diffusion()
        self.move()
        self.check_all_collisions()
        self.update_militants()
        self.clear_screen()
        self.draw()
        self.check_pause()
        self.handle_events()
        self.show_ammunition()
        self.time_tick(FPS)
      pygame.quit()
  
  def check_pause(self):
      if self._game_paused == True: 
          self.pause_screen()

  def pause_screen(self):
      font = pygame.font.Font(None, 72)  
      text = font.render("RESUME", True, (255, 255, 255))  
      text_rect = text.get_rect()
      BUTTON_WIDTH, BUTTON_HEIGHT = text_rect.width + 60, text_rect.height + 60  
      button = pygame.Rect((self._screen_width - BUTTON_WIDTH) // 2, (self._screen_height - BUTTON_HEIGHT) // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
      text_rect.center = button.center
      
      while self._game_paused:
          for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button.collidepoint(event.pos):
                        self._screen.fill(BLACK)
                        self._game_paused = False
                        self._moving_down, self._moving_left, self._moving_right, self._moving_up = False, False, False, False
                        return
          self._screen.fill((255, 255, 255))  
          pygame.draw.rect(self._screen, (39, 58, 152), button)  
          self._screen.blit(text,text_rect)
          pygame.display.flip()  
  
  def handle_events(self):
      for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            self._running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._game_paused = True

            if event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.key == pygame.K_w:
                self._player.move(0, -1)
                self._moving_up = True
            elif event.key == pygame.K_a:
                self._player.move(-1,0)
                self._moving_left = True
            elif event.key == pygame.K_s:
                self._player.move(0,1)
                self._moving_down = True
            elif event.key == pygame.K_d:
                self._player.move(1,0)
                self._moving_right = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self._player.move(0, -1)
                self._moving_up = False
            elif event.key == pygame.K_a:
                self._player.move(-1,0)
                self._moving_left = False
            elif event.key == pygame.K_s:
                self._player.move(0,1)
                self._moving_down = False
            elif event.key == pygame.K_d:
                self._player.move(1,0)
                self._moving_right = False
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if self._player._bullets >= 1:
            target_x, target_y = pygame.mouse.get_pos()
            self._player.shoot(target_x,target_y)    
  def diffusion(self):
        current_time = pygame.time.get_ticks()
        self._last_time_since_diffusion = current_time - self._last_diffusion
        if self._last_time_since_diffusion >= self._diffusion_freq:
          self._militia_group.diffusion()
          self._last_diffusion = current_time

 

  def check_all_collisions(self):           
      self.handle_bullet_hits()           
      self.handle_recruitment() 
      self.handle_comprimises()
      self.handle_assassinations()
      self.handle_supply()

  def handle_bullet_hits(self):
    hit_dict = self._bullets_group.did_your_group_collide_with(self._militia_group)
    for damaged_militant in hit_dict.keys():
        impacted_bullets = hit_dict[damaged_militant]
        for bullet in impacted_bullets:
            bullet.hit_militant(damaged_militant)
  
  def handle_recruitment(self):
    recruit_dict = self._citizens_group.did_your_group_collide_with(self._militia_group)
    for militant in recruit_dict.keys():
            recruited_citizens = recruit_dict[militant]
            for citizen in recruited_citizens:
                new_militant = citizen.turn_to_militant(self._militia_group)
                citizen.remove()
                self._militia_group.recruit(new_militant, self._links_group)

  def handle_comprimises(self):
    comprimise_dict = self._militia_group.did_your_group_collide_with(self._player)
    for militant_that_caught_the_player in comprimise_dict.keys():
        idea_bool = militant_that_caught_the_player.are_you_communist()
        if idea_bool:
            self._running = False
        else: continue

  def handle_assassinations(self):
        assassination_dict = self._assassins_group.did_your_group_collide_with(self._player)
        if assassination_dict:
            self._running = False

  def handle_supply(self):    
    is_player_in = self._warehouse.check_your_individual_collision_with(self._player)
    if not is_player_in:
        self._warehouse.reset_stats()

    else: self._warehouse.supply(self._player)

 
  def clear_screen(self):
        self._screen.fill(BLACK)


  def draw(self):
    self._all_sprites_group.draw()   


  def time_tick(self, FPS):
      self._clock.tick(FPS)
      pygame.display.flip()


  def update_militants(self):   
      self._militia_group.update_radius_and_color()
  
  def move(self):   
      self._player.you_keep_moving(self._moving_right, self._moving_left, self._moving_up, self._moving_down)
      
      self._cpu_player.doctrinate_your_militants()

      self._militia_group.move()

      self._assassins_group.hunt_down(self._player)

      self._bullets_group.move()



  def show_ammunition(self):
        self._player.display_your_ammunition()

      
  


class Sprite():
    def __init__(self, color, radius, group, screen, x = None, y = None, shape = "circle"):
        self._screen = screen
        self._screen_height = self._screen.get_height()
        self._screen_width = self._screen.get_width()

        if x == None:
            x = random.randint(0, self._screen_width - 20)

        if y == None:
            y = random.randint(0, self._screen_height - 20)

        self._color = color
        self._radius = radius
        self._group = group
        self._group.add(self)

        if shape == "circle":
          self.image = pygame.Surface([self._radius*2, self._radius*2], pygame.SRCALPHA)
          pygame.draw.circle(self.image, self._color, (self._radius, self._radius), self._radius)
          self.rect = self.image.get_rect()
          self.rect.centerx = x
          self.rect.centery = y

        if shape == "square":
            self.image = pygame.Surface((self._radius, self._radius))
            pygame.draw.rect(self.image, self._color, [0, 0, self._radius, self._radius])
            self.rect = self.image.get_rect()
            self.rect.centerx = self._screen_width / 2
            self.rect.centery = self._screen_height - self._radius
       
        self.rect.centerx = x
        self.rect.centery = y

    
    def check_your_individual_collision_with(self,other_sprite):
        my_pos = pygame.math.Vector2(self.rect.center)
        return other_sprite.did_we_collide(my_pos, self._radius)
  
    def did_we_collide(self, other_sprite_pos, other_sprite_rad):
        my_pos = pygame.math.Vector2(self.rect.center)
        if my_pos.distance_to(other_sprite_pos) <= self._radius + other_sprite_rad:
            return True
        

    def draw(self):
        self._screen.blit(self.image, self.rect)

    def remove(self):
        self._group.remove_me(self)

 

class MovingObject(Sprite):
  
  def __init__(self, color, speed, group, screen, radius = 10, x = None, y = None):
      super().__init__(color, radius, group, screen, x = x, y = y)
      self._speed = speed
      self._dx = None
      self._dy = None

  def move(self):
       
       self.rect.centerx += self._speed * self._dx
       self.rect.centery += self._speed * self._dy   
       self.check_boundaries() 

  def check_boundaries(self):
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.rect.x += self._speed * - self._dx
      
        if self.rect.right > self._screen_width:
            self.rect.right = self._screen_width
            self.rect.x += self._speed * - self._dx
      
        if self.rect.top < 0:
            self.rect.top = 0
            self.rect.y += self._speed * - self._dy
      
        if self.rect.bottom > self._screen_height:
            self.rect.bottom = self._screen_height
            self.rect.y += self._speed * - self._dy

  def be_chased_by(self, caller):
      caller.set_direction(self.rect.centerx, self.rect.centery)

  def set_direction(self, target_x, target_y):
        direction = pygame.math.Vector2(target_x - self.rect.centerx, target_y - self.rect.centery)
        direction.normalize_ip()
        self._dx, self._dy = direction.x, direction.y
      



class Link(Sprite):
  def __init__(self, from_, to_, group, screen):
      super().__init__(WHITE, 1, group, screen)
      self._from = from_
      self._to = to_
  def draw(self):
    pygame.draw.aaline(self._screen, (255,255,255,0), self._from.rect.center, self._to.rect.center, blend = True)


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

class Citizen(Sprite):
    def __init__(self, color, radius, group, screen):
        super().__init__(color, radius, group, screen)

    def turn_to_militant(self, militia_group):
        new_militant = Militant(RED, 1, militia_group, self._screen, self.rect.centerx, self.rect.centery)
        return new_militant

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
        if time_since_last_shot >= 550:
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
          if self._ideology >= -16.5:
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

        


my_game = Game(2, 200, 1, 1200)
my_game.run()



