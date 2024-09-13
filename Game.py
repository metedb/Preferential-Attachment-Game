import pygame
import random
import numpy as np

pygame.init()
pygame.font.init()

from main import BaseGroup, Militia, SpriteGroup, Warehouse, Militant, CPU_Player, Player, Citizen, MovingObject, BLACK, WHITE, RED, BROWN


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
      player = Player(WHITE, 2, 20, 5, self._all_sprites_group, self._bullets_group, self._screen)
      self._player = player
      cpu_player = CPU_Player(WHITE, -2,float('inf'), 5, self._all_sprites_group, self._bullets_group, self._militia_group, self._screen)
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
    for link in self._links_group._sprites:
        link.draw()

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

