import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
coin_score = 0
timer = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("10/racer/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80)
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[pygame.K_UP]:
        #     self.rect = self.rect.move(0, -5)
        # if pressed_keys[pygame.K_DOWN]:
        #     self.rect = self.rect.move(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect = self.rect.move(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect = self.rect.move(5, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("10/racer/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, 60)

    def update(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("10/racer/Coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, 60)

    def update(self):
        self.rect.move_ip(0, SPEED+3)
        if (self.rect.top > SCREEN_HEIGHT):
            self.rect.top = 0
            
        
    def collide(self):
        global coin_score
        coin_score += 1
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def draw(self, surface):
        surface.blit(self.image, self.rect)




background = pygame.image.load("10/racer/AnimatedStreet.png")
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ball = Player()
wall = Enemy()
coin = Coin()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

all_sprites.add(ball)
all_sprites.add(wall)
all_sprites.add(coin)
enemies.add(wall)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

running = True
Coin.update(coin)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == INC_SPEED:
            SPEED += 3
    
    DISPLAY.blit(background, (0, 0))
    text = font.render(str(SCORE), True, (0, 0, 0))
    DISPLAY.blit(text, (10, 10))
    text = font.render(str(coin_score), True, (0, 0, 0))
    DISPLAY.blit(text, (360, 10))

    for sprite in all_sprites:
        sprite.update()
        sprite.draw(DISPLAY)
    if pygame.sprite.collide_rect(ball, wall):
        DISPLAY.fill((255, 0, 0))
        # timer.delay(2000)
        running = False
    if pygame.sprite.collide_rect(ball, coin):
        Coin.collide(coin)
        Coin.update(coin)

    pygame.display.update()
    timer.tick(60)


pygame.quit()