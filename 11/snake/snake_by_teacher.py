import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

window_width = 500
window_height = 500

cell_length = 20

score_font = pygame.font.SysFont("comicsansms", 35)
food_font = pygame.font.SysFont("comicsansms", 15)

display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

class Food:
    x = 0
    y = 0
    weight = 10
    spawn_time = 0

    def __init__(self):
        x_food = random.randint(0, window_width - cell_length)
        x_food = x_food - (x_food % 20)
        y_food = random.randint(0, window_width - cell_length)
        y_food = y_food - (y_food % 20)

        self.x = x_food
        self.y = y_food
        self.weight = 10
        self.spawn_time = pygame.time.get_ticks()

    def respawn(self):
        x_food = random.randint(0, window_width - cell_length)
        x_food = x_food - (x_food % 20)
        y_food = random.randint(0, window_width - cell_length)
        y_food = y_food - (y_food % 20)
        self.x = x_food
        self.y = y_food
        self.spawn_time = pygame.time.get_ticks()
        self.weight = 10

    def update_weight(self):
        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - self.spawn_time) // 1000
        if elapsed_seconds >= 9:
            self.respawn()
        else:
            self.weight = 10 - elapsed_seconds

    def draw(self):
        self.update_weight()
        pygame.draw.rect(display, GREEN, [self.x, self.y, cell_length, cell_length])
        weight_text = food_font.render(str(self.weight), True, BLACK)
        text_rect = weight_text.get_rect(center=(self.x + cell_length // 2, self.y + cell_length // 2))
        display.blit(weight_text, text_rect)

class Snake:
    body = []
    x_head = 0
    y_head = 0
    size = 1
    x_change = 0
    y_change = 0
    score = 0

    is_alive = True

    def __init__(self):
        x_snake = window_width / 2
        x_snake = x_snake - (x_snake % 20)
        y_snake = window_height / 2
        y_snake = y_snake - (y_snake % 20)
        self.x_head = x_snake
        self.y_head = y_snake
        self.size = 1
        self.score = 0
    
    def move_direction(self, direction):
        if direction == pygame.K_UP:
            self.y_change = -cell_length
            self.x_change = 0
        elif direction == pygame.K_DOWN:
            self.y_change = cell_length
            self.x_change = 0
        elif direction == pygame.K_LEFT:
            self.x_change = -cell_length
            self.y_change = 0
        elif direction == pygame.K_RIGHT:
            self.x_change = cell_length
            self.y_change = 0

    
    def draw(self):
        self.x_head += self.x_change
        self.y_head += self.y_change

        if self.x_head < 0 or self.x_head >= window_width:
            self.is_alive = False
            return
        if self.y_head < 0 or self.y_head >= window_height:
            self.is_alive = False
            return
        
        self.body.append([self.x_head, self.y_head])
        if len(self.body) > self.size:
            self.body.pop(0)
        
        if [self.x_head, self.y_head] in self.body[:-1]:
            self.is_alive = False
            return
        
        for i in self.body:
            pygame.draw.rect(display, BLACK, [i[0], i[1], cell_length, cell_length])
    

def game():
    snake = Snake()
    food = Food()
    start_time = pygame.time.get_ticks()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                snake.move_direction(event.key)
        
        if snake.is_alive == False:
            pygame.quit()
            return
        display.fill(BLUE)
        current_time = (pygame.time.get_ticks() - start_time) // 1000
        score_text = score_font.render("Score: " + str(snake.score) + " Time: " + str(current_time), True, YELLOW)
        display.blit(score_text, [0, 0])
        snake.draw()
        
        if snake.x_head == food.x and snake.y_head == food.y:
            snake.score += food.weight
            snake.size += 1
            food = Food()
        
        food.draw()
        pygame.display.update()
        clock.tick(10)

game()