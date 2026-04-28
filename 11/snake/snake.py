import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
BORDER_SIZE = 40
SPEED = 5
MOVE_SPEED = 2  #скорость в пикселях
FPS = 120
SCORE = 0
LEVEL = 1
coin_score = 0
timer = pygame.time.Clock()
game_over = False

font = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 32, bold=True)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("10/snake/snake.png")
        # Уменьшение в 2 раза
        self.original_image = pygame.transform.scale(original_image, (int(original_image.get_width() * 0.5), int(original_image.get_height() * 0.5)))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.direction_x = MOVE_SPEED  
        self.direction_y = 0
        self.rotation = 0  # 0=right, 90=up, 180=left, 270=down
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            self.direction_x = 0
            self.direction_y = -MOVE_SPEED
            self.rotation = 90
        elif pressed_keys[pygame.K_DOWN]:
            self.direction_x = 0
            self.direction_y = MOVE_SPEED
            self.rotation = 270
        elif pressed_keys[pygame.K_LEFT]:
            self.direction_x = -MOVE_SPEED
            self.direction_y = 0
            self.rotation = 180
        elif pressed_keys[pygame.K_RIGHT]:
            self.direction_x = MOVE_SPEED
            self.direction_y = 0
            self.rotation = 0
        
        # безостановочное движеине
        self.rect.x += self.direction_x
        self.rect.y += self.direction_y
        
    
    def update_image(self):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def check_borders(self):
        global game_over
        if self.rect.left <= BORDER_SIZE or self.rect.right >= SCREEN_WIDTH - BORDER_SIZE or self.rect.top <= BORDER_SIZE or self.rect.bottom >= SCREEN_HEIGHT - BORDER_SIZE:
            game_over = True
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        # столкнулся ли он с границей
        self.check_borders()
        
        # поворот головы
        self.update_image()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("10/racer/Coin.png")
        self.image = pygame.transform.scale(original_image, (int(original_image.get_width() * 0.4), int(original_image.get_height() * 0.4)))
        self.rect = self.image.get_rect()
        self.spawn_random()
    
    def spawn_random(self):
        #спавн еды
        self.rect.center = (random.randint(BORDER_SIZE + 40, SCREEN_WIDTH - BORDER_SIZE - 40), random.randint(BORDER_SIZE + 40, SCREEN_HEIGHT - BORDER_SIZE - 40))
    
    def collide(self):
        global coin_score, SCORE, LEVEL, SPEED, MOVE_SPEED
        coin_score += 1
        SCORE += 10
        
        # увелничение скорости и уровня
        new_level = SCORE // 30 + 1
        if new_level > LEVEL:
            LEVEL = new_level
            MOVE_SPEED += 0.5
        
        self.spawn_random()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)




background = pygame.image.load("10/racer/AnimatedStreet.png")
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Extended Edition")

ball = Player()
coin = Coin()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

all_sprites.add(ball)
all_sprites.add(coin)


running = True
Coin.update(coin)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                #перезапуск
                ball.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                ball.direction_x = 0
                ball.direction_y = 0
                coin.spawn_random()
                SCORE = 0
                LEVEL = 1
                coin_score = 0
                MOVE_SPEED = 2
                game_over = False
    
    # фон
    DISPLAY.fill((255, 255, 255))
    
    # границы
    pygame.draw.rect(DISPLAY, (200, 0, 0), (0, 0, SCREEN_WIDTH, BORDER_SIZE), 0)
    pygame.draw.rect(DISPLAY, (200, 0, 0), (0, SCREEN_HEIGHT - BORDER_SIZE, SCREEN_WIDTH, BORDER_SIZE), 0)
    pygame.draw.rect(DISPLAY, (200, 0, 0), (0, 0, BORDER_SIZE, SCREEN_HEIGHT), 0)
    pygame.draw.rect(DISPLAY, (200, 0, 0), (SCREEN_WIDTH - BORDER_SIZE, 0, BORDER_SIZE, SCREEN_HEIGHT), 0)
    
    # счёт
    text = font.render(f"Score: {SCORE}", True, (0, 0, 0))
    DISPLAY.blit(text, (10, 10))
    
    # уровень
    text_level = font.render(f"Level: {LEVEL}", True, (0, 0, 0))
    DISPLAY.blit(text_level, (10, 35))
    
    # съедено еды
    text_coins = font.render(f"Foods: {coin_score}", True, (0, 0, 0))
    DISPLAY.blit(text_coins, (SCREEN_WIDTH - 150, 10))
    
    # скорость
    text_speed = font.render(f"Speed: {MOVE_SPEED}", True, (0, 0, 0))
    DISPLAY.blit(text_speed, (SCREEN_WIDTH - 150, 35))

    if not game_over:
        for sprite in all_sprites:
            sprite.update()
            sprite.draw(DISPLAY)
            
        if pygame.sprite.collide_rect(ball, coin):
            Coin.collide(coin)
            Coin.update(coin)
    else:
        # отрисовка экрана "Game Over"
        for sprite in all_sprites:
            sprite.draw(DISPLAY)
        
        game_over_text = font_big.render("GAME OVER!", True, (200, 0, 0))
        restart_text = font.render("Press R to restart", True, (0, 0, 0))
        DISPLAY.blit(game_over_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 40))
        DISPLAY.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
        MOVE_SPEED = 2

    pygame.display.update()
    timer.tick(FPS)


pygame.quit()