import pygame
from pygame.locals import *
import random

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
fps = 30
screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Oi Kire")


rows  = 3
cols = 5
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()

red = (255,0,0)
green = (0,255,0)

bg = pygame.image.load('../image/bg.png')
def draw_bg():
    screen.blit(bg, (0,0))
    
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x,y,  health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../image/jado.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)

               
    def update(self):
        speed = 8
        cooldown = 300
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed  
            
        time_now = pygame.time.get_ticks()    
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx,self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
            
            
            self.mask = pygame.mask.from_surface(self.image)
            
        pygame.draw.rect(screen, red, (self.rect.x, self.rect.bottom + 10, self.rect.width, 15))
        if self.health_remaining > 0:
            health_bar_width = int(self.rect.width * (self.health_remaining / self.health_start))
            pygame.draw.rect(screen, green, (self.rect.x, self.rect.bottom + 10, health_bar_width, 15))

        if self.health_remaining <= 0:
            self.kill()
            print("Spaceship destroyed! Game Over.")
    
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../image/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y] 
        self.mask = pygame.mask.from_surface(self.image)      
        
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 100:
            self.kill()
        hit_alien = pygame.sprite.spritecollide(self, alien_group, True)
        if hit_alien:
            self.kill()
        
            
            
                      
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../image/kawla.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_counter = 0
        self.move_direction = 1
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction        
    
    
               
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../image/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]  
        self.mask = pygame.mask.from_surface(self.image)
     
        
    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()   
                     
        hits = pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask)
        if hits:
            self.kill()
            for spaceship in hits:               
              spaceship.health_remaining -= 1
            print("Hit spaceship! Health now:", spaceship.health_remaining)
   
   
        
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

 
def  create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)
            
create_aliens()
         

spaceship = Spaceship(int(screen_width / 2), screen_height - 100,4)
spaceship_group.add(spaceship)

font = pygame.font.SysFont(None,60)

    
run = True
while run:
    
    clock.tick(fps)
    draw_bg()
    
    time_now = pygame.time.get_ticks()
    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
            
    spaceship.update()  
    bullet_group.update() 
    alien_group.update() 
    alien_bullet_group.update()
    
    if len(spaceship_group) == 0:
       
        screen.fill((0, 0, 0)) 
        text = font.render('GAME OVER', True, red)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)  
        run = False
            
    spaceship_group.draw(screen) 
    bullet_group.draw(screen)   
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
            
    pygame.display.update()
pygame.quit()
        