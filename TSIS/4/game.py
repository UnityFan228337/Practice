import pygame
import random
import db
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

score_font = pygame.font.SysFont("comicsansms", 20)
food_font = pygame.font.SysFont("comicsansms", 15)

display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

class Food:
    x = 0
    y = 0
    weight = 10
    spawn_time = 0

    def __init__(self, bad=False):
        x_food = random.randint(0, window_width - cell_length)
        x_food = x_food - (x_food % 20)
        y_food = random.randint(0, window_width - cell_length)
        y_food = y_food - (y_food % 20)
        self.x = x_food
        self.y = y_food
        self.weight = 10
        self.bad = False
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
    def draw_bad(self):
        self.update_weight()
        pygame.draw.rect(display, RED, [self.x, self.y, cell_length, cell_length])
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
        self.body = []
        self.size = 1
        self.score = 0
        self.x_change = 0
        self.y_change = 0
        self.is_alive = True

    def deviding(self):
        if self.size > 2:
            self.body = self.body[:len(self.body) // 2]
            self.size /= 2
        else:
            self.is_alive = False

    def move_direction(self, direction):
        if direction == pygame.K_UP and self.y_change == 0:
            self.y_change = -cell_length
            self.x_change = 0
        elif direction == pygame.K_DOWN and self.y_change == 0:
            self.y_change = cell_length
            self.x_change = 0
        elif direction == pygame.K_LEFT and self.x_change == 0:
            self.x_change = -cell_length
            self.y_change = 0
        elif direction == pygame.K_RIGHT and self.x_change == 0:
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


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hover = False
        self.font = pygame.font.SysFont(None, 36)  # шрифт создаётся один раз

    def draw(self, surface):
        color = (100, 150, 255) if self.hover else (0, 100, 255)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def enter_name():
    name = ""
    input_font = pygame.font.SysFont("comicsansms", 28)
    label_font = pygame.font.SysFont("comicsansms", 22)
    confirm_button = Button(window_width // 2 - 100, window_height // 2 + 60, 200, 50, "OK")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEMOTION:
                confirm_button.update(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_button.is_clicked(event.pos) and name.strip():
                    return name.strip()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 16 and event.unicode.isprintable():
                        name += event.unicode

        display.fill(BLACK)
        label = label_font.render("Enter your nickname:", True, YELLOW)
        display.blit(label, (window_width // 2 - label.get_width() // 2, window_height // 2 - 80))

        input_rect = pygame.Rect(window_width // 2 - 120, window_height // 2 - 30, 240, 45)
        pygame.draw.rect(display, WHITE, input_rect, 2)
        name_text = input_font.render(name, True, WHITE)
        display.blit(name_text, (input_rect.x + 8, input_rect.y + 8))

        confirm_button.draw(display)
        pygame.display.update()
        clock.tick(60)


def menu():
    start_button = Button(window_width // 2 - 100, window_height // 2 - 25, 200, 50, "Start Game")
    leaderboard_button = Button(window_width // 2 - 100, window_height // 2 + 50, 200, 50, "Leaderboard")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEMOTION:
                start_button.update(event.pos)
                leaderboard_button.update(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    nickname = enter_name()
                    if nickname is None:
                        return None
                    result = game(nickname)
                    return result
                if leaderboard_button.is_clicked(event.pos):
                    leaderboard_rows = db.launch(1)
                    return leaderboard(leaderboard_rows)

        display.fill(BLACK)
        start_button.draw(display)
        leaderboard_button.draw(display)
        pygame.display.update()
        clock.tick(60)


def leaderboard(rows):
    display.fill(BLACK)
    back = Button(0, 0, 200, 50, "Back")
    title_font = pygame.font.SysFont("comicsansms", 40)
    title_text = title_font.render("Leaderboard", True, YELLOW)
    display.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 20))

    for index, row in enumerate(rows):
        player_text = score_font.render(f"{index + 1}. {row[1]} - Score: {row[2]} - Level: {row[3]} - Time: {row[4]}", True, WHITE)
        if index == 10:
            break
        display.blit(player_text, (10, 80 + index * 40))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                back.update(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.is_clicked(event.pos):
                    return menu()

            back.draw(display)
            pygame.display.update()


def game(nickname="Player"):
    snake = Snake()
    food = Food()
    bad_food = Food(bad=True)
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                snake.move_direction(event.key)

        if not snake.is_alive:
            # НЕ вызываем pygame.quit() — это делает main.py
            return snake.score, nickname

        display.fill(BLUE)
        current_time = (pygame.time.get_ticks() - start_time) // 1000
        score_text = score_font.render(f"{nickname} | Score: {snake.score} Time: {current_time}", True, YELLOW)
        display.blit(score_text, [0, 0])
        snake.draw()

        if snake.x_head == food.x and snake.y_head == food.y:
            snake.score += food.weight
            snake.size += 1
            food.respawn()
            bad_food.respawn()
        elif snake.x_head == bad_food.x and snake.y_head == bad_food.y:
            snake.deviding()
            food.respawn()
            bad_food.respawn()
        food.draw()
        bad_food.draw_bad()
        pygame.display.update()
        clock.tick(10)
