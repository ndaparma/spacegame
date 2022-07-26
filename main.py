# https://realpython.com/pygame-a-primer/#note-on-sources
# https://stackoverflow.com/questions/66088144/pygame-bullet-movement
import pygame
import random

#import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

#define constants for screen 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = ((255, 255, 255))
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)


pygame.init()
clock = pygame.time.Clock()

score = 0
iframes = 6000
POWERUP_TIME = 6000
POWERUP_TIME2 = 4000
#setup groups

all_sprites = pygame.sprite.LayeredUpdates()
player = pygame.sprite.Group()
lasers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
planets = pygame.sprite.Group()
bombs = pygame.sprite.Group()
powers = pygame.sprite.Group()



class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('bgimg.png').convert()
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = self.rectBGimg.width

        self.moving_speed = 5

    def update(self):
        self.bgX1 -= self.moving_speed
        self.bgX2 -= self.moving_speed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width

    def render(self):
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))


#Game objects/Player

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self._layer = 3
        pygame.sprite.Sprite.__init__(self, all_sprites, player)
        self.surf = pygame.image.load("ship.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(
            0,
            300,
        ))
        self.power = 0
        self.power_time = pygame.time.get_ticks()
        self.power2 = 0
        self.power_time2 = pygame.time.get_ticks()
        self.HP = 1
        self.MaxHP = 3
        self.inv_time = pygame.time.get_ticks()
        self.inv_active = 0

      
    def update(self, pressed_keys):
        current_time = pygame.time.get_ticks()

        if self.HP > 1:
          self.surf = pygame.image.load("ship2.png").convert_alpha()
        if self.HP == 1:
          self.surf = pygame.image.load("ship.png").convert_alpha()

        if self.power >= 1 and current_time > self.power_time + POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
          
        if self.power2 >= 1 and current_time > self.power_time2 + POWERUP_TIME:
            self.power2 -= 1
            self.power_time2 = pygame.time.get_ticks()
          
        if self.inv_active >= 1 and current_time > self.inv_time + iframes:
            self.inv_active -= 1
            self.inv_time = pygame.time.get_ticks()
      
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -15)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 15)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-15, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(15, 0)
        if pressed_keys[K_SPACE] and self.power2 >= 1:
            player.shoot()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    def damage(self):
     if self.inv_active == 0:
        self.HP -= 1
        self.inv_active = 1
     else:
       pass

    def shoot(self):
        if self.power == 0:
          laser = Laser(self.rect.centerx, self.rect.centery)
          all_sprites.add(laser)
          lasers.add(laser)
        elif self.power == 1:
          laser = Laser(self.rect.centerx, self.rect.top)
          laser2 = Laser(self.rect.centerx, self.rect.bottom)
          all_sprites.add(laser)
          all_sprites.add(laser2)
          lasers.add(laser)
          lasers.add(laser2)
        elif self.power >= 2:
          laser = Laser(self.rect.centerx, self.rect.top)
          laser2 = Laser(self.rect.centerx, self.rect.bottom)
          laser3 = Laser(self.rect.centerx, self.rect.centery)
          all_sprites.add(laser)
          all_sprites.add(laser2)
          all_sprites.add(laser3)
          lasers.add(laser)
          lasers.add(laser2)
          lasers.add(laser3)

    def powerup1(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    def powerup2(self):
        self.power2 += 1
        self.power_time2 = pygame.time.get_ticks()
    def powerup3(self):
        if self.HP < self.MaxHP:
          self.HP += 1
        else:
          pass


enemy_images = ["astroid1.png", "astroid2.png", "astroid3.png"]


class Astroid(pygame.sprite.Sprite):
    def __init__(self):
        super(Astroid, self).__init__()
        self._layer = 2
        self.type = 'astroid'
        pygame.sprite.Sprite.__init__(self, all_sprites, enemies)
        self.surf = pygame.image.load(random.choice(enemy_images)).convert_alpha()
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
        ))
        self.speed = random.randint(5, 20)
        self.points = 25
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super(Alien, self).__init__()
        self._layer = 2
        self.type = 'alien'
        pygame.sprite.Sprite.__init__(self, all_sprites, enemies)
        self.surf = pygame.image.load('alien.png')
        self.rect = self.surf.get_rect(center=(
            random.randint(0, SCREEN_WIDTH),
            random.randint(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100),
        ))
        self.speed = 25
        self.points = 1000

      
    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.bottom < 0:
            self.kill()

planet_images = ['planet1.png','planet2.png','planet3.png','spacecat.png',]
class Planets(pygame.sprite.Sprite):
    def __init__(self):
        super(Planets, self).__init__()
        self._layer = 1
        pygame.sprite.Sprite.__init__(self, all_sprites, planets)
        self.surf = pygame.image.load(random.choice(planet_images)).convert_alpha()
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
        ))

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super(Bomb, self).__init__()
        self._layer = 2
        pygame.sprite.Sprite.__init__(self, all_sprites, bombs)
        self.surf = pygame.image.load("bomb.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
        ))

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Extrashot(pygame.sprite.Sprite):
    def __init__(self):
        super(Extrashot, self).__init__()
        self._layer = 2
        self.type = 'extra_shot'
        pygame.sprite.Sprite.__init__(self, all_sprites, powers)
        self.surf = pygame.image.load("power_up.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
        ))

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Rapidshot(pygame.sprite.Sprite):
    def __init__(self):
        super(Rapidshot, self).__init__()
        self._layer = 2
        self.type = 'rapid_shot'
        pygame.sprite.Sprite.__init__(self, all_sprites, powers)
        self.surf = pygame.image.load("power_up2.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
        ))

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class HPup(pygame.sprite.Sprite):
    def __init__(self):
        super(HPup, self).__init__()
        self._layer = 2
        self.type = 'hp_up'
        pygame.sprite.Sprite.__init__(self, all_sprites, powers)
        self.surf = pygame.image.load("power_up3.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
        ))

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self._layer = 2
        pygame.sprite.Sprite.__init__(self, all_sprites, lasers)
        self.surf = pygame.image.load("laser.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 20

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.kill()



# events for adding objects
ADDASTROID = pygame.USEREVENT + 1
pygame.time.set_timer(ADDASTROID, 250)
ADDPLANET = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLANET, 3700)
ADDBOMB = pygame.USEREVENT + 3
pygame.time.set_timer(ADDBOMB, 27000)
ADDEXTRASHOT = pygame.USEREVENT + 4
pygame.time.set_timer(ADDEXTRASHOT, 5500)
ADDALIEN= pygame.USEREVENT + 5
pygame.time.set_timer(ADDALIEN, 1500)
ADDRAPIDSHOT = pygame.USEREVENT + 6
pygame.time.set_timer(ADDRAPIDSHOT, 17250)
ADDHPUP = pygame.USEREVENT + 7
pygame.time.set_timer(ADDHPUP, 22350)


# Instantiate player/BG
player = Player()
back_ground = Background()


running = True
# Main loop
while running:

    # Look at every event in the queue
    for event in pygame.event.get():
        # Check if user hit key
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                player.shoot()

        # Closes game with window X
        elif event.type == QUIT:
            running = False

        #Add a game objects
        elif event.type == ADDASTROID:
            # Create the new enemy and add it to sprite groups
            new_astroid = Astroid()
            enemies.add(new_astroid)
            all_sprites.add(new_astroid)

        elif event.type == ADDPLANET:
            new_planet = Planets()
            planets.add(new_planet)
            all_sprites.add(new_planet)

        elif event.type == ADDBOMB:
            new_bomb = Bomb()
            bombs.add(new_bomb)
            all_sprites.add(new_bomb)

        elif event.type == ADDEXTRASHOT:
            new_extrashot = Extrashot()
            powers.add(new_extrashot )
            all_sprites.add(new_extrashot )

        elif event.type == ADDRAPIDSHOT:
            new_rapidshot = Rapidshot()
            powers.add(new_rapidshot )
            all_sprites.add(new_rapidshot )

        elif event.type == ADDHPUP:
            new_hpup = HPup()
            powers.add(new_hpup)
            all_sprites.add(new_hpup)

        elif event.type == ADDALIEN and score >= 3000:
            new_alien = Alien()
            enemies.add(new_alien)
            all_sprites.add(new_alien)
    # Get the set of keys pressed and check for user input/ Update plaer pos
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    # Update objects pos
    enemies.update()
    planets.update()
    bombs.update()
    lasers.update()
    powers.update()


    # Draw all sprites
    back_ground.update()
    back_ground.render()
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.surf, entity.rect)

    #Collision checks
      
    # Check if any enemies have collided with the player
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.damage()
        if player.HP <= 0:    
          player.kill()
          running = False
        else:
          pass

    #check if bombs collided with plaer
    if pygame.sprite.spritecollide(player, bombs, True):
        score += 500
        #checks for all new_astroid sprites in enemies group and kills all
        for new_astroid in enemies:
            new_astroid.kill()
        for new_alien in enemies:
            new_alien.kill()
          
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
      if hit.type == 'extra_shot':
        score += 50
        player.powerup1()
      if hit.type == 'rapid_shot':
        score += 100
        player.powerup2()
      if hit.type == 'hp_up':
        score += 200
        player.powerup3()


    #checks if lasers collide with enemies, kills both and increases score
    hits = pygame.sprite.groupcollide(enemies, lasers, True, True)  
    for hit in hits:
      if hit.type == "astroid":
          score += 25
      elif hit.type == "alien":
          score += 100
        
        

    # Update the display
    pygame.display.flip()
    clock.tick(30)
    #Update/ display score
    pygame.display.set_caption(f"Score:{score}")
    score += 1
