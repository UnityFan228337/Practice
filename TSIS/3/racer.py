import pygame
import random
import json
import os
from enum import Enum
from datetime import datetime

pygame.init()

#variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
LANES = 3
LANE_WIDTH = SCREEN_WIDTH // LANES
BASE_SPEED = 3
MAX_SPEED = 12
SCORE = 0
COIN_SCORE = 0
DIFFICULTY_MULTIPLIER = 1.0
GAME_OVER = False
timer = pygame.time.Clock()
font_large = pygame.font.SysFont("Verdana", 32, bold=True)
font_small = pygame.font.SysFont("Verdana", 16)
font_medium = pygame.font.SysFont("Verdana", 20)
font_huge = pygame.font.SysFont("Verdana", 48, bold=True)

#folder
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

#loading
background_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "background.wav"))
crash_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "crash.wav"))

def update_audio_settings():
    global background_sound, crash_sound
    if settings["music_enabled"]:
        background_sound.set_volume(settings["music_volume"])
    else:
        background_sound.set_volume(0)
    
    if settings["sound_enabled"]:
        crash_sound.set_volume(settings["sound_volume"])
    else:
        crash_sound.set_volume(0)

# ============= SETTINGS =============
def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"music_enabled": True, "music_volume": 0.3, "sound_enabled": True, "sound_volume": 0.7}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    except:
        pass

settings = load_settings()

update_audio_settings()  # Apply initial settings

player_img = pygame.image.load(os.path.join(ASSETS_PATH, "Player.png"))
player_img = pygame.transform.scale(player_img, (60, 60))  # Scale player car to square
enemy_img = pygame.image.load(os.path.join(ASSETS_PATH, "Enemy.png"))
coin_img = pygame.image.load(os.path.join(ASSETS_PATH, "Coin.png"))
background_img = pygame.image.load(os.path.join(ASSETS_PATH, "AnimatedStreet.png"))

DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game - Enhanced")

# ============= LEADERBOARD FILE =============
LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard.json")

# ============= SETTINGS FILE =============
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

# ============= BUTTON CLASS =============
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hover = False
    
    def draw(self, surface):
        color = (100, 150, 255) if self.hover else (0, 100, 255)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        text_surface = font_medium.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def save_score(username, score, distance, coins):
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                leaderboard = json.load(f)
        else:
            leaderboard = []
        
        # Create unique entry
        import time
        new_entry = {
            "name": username,
            "score": score,
            "distance": distance,
            "coins": coins,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": int(time.time())
        }
        
        leaderboard.append(new_entry)
        
        # Sort by score descending and keep only top 20
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        leaderboard = leaderboard[:20]
        
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving score: {e}")

# ============= POWER-UP CLASS =============
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, lane, power_type):
        super().__init__()
        self.power_type = power_type
        self.lane = lane
        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.rect.y = -30
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 8000
    
    def create_image(self):
        self.image = pygame.Surface((30, 30))
        if self.power_type == "nitro":
            self.image.fill((255, 255, 0))
            pygame.draw.polygon(self.image, (255, 165, 0), [(15, 5), (25, 25), (5, 25)])
        elif self.power_type == "shield":
            self.image.fill((0, 100, 255))
            pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 12, 2)
        elif self.power_type == "repair":
            self.image.fill((0, 255, 0))
            pygame.draw.rect(self.image, (255, 255, 255), (10, 8, 10, 14))
            pygame.draw.rect(self.image, (255, 255, 255), (8, 10, 14, 10))
    
    def update(self):
        self.rect.y += 4
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.lane = LANES // 2  # Start in middle lane
        self.set_lane_position()
        self.rect.y = SCREEN_HEIGHT - 90
        self.lane_change_delay = 0
        self.shield_active = False
        self.nitro_active = False
        self.nitro_time = 0
    
    def set_lane_position(self):
        self.rect.centerx = self.lane * LANE_WIDTH + LANE_WIDTH // 2
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.lane_change_delay -= 1
        
        if self.lane_change_delay <= 0:
            if pressed_keys[pygame.K_LEFT] and self.lane > 0:
                self.lane -= 1
                self.set_lane_position()
                self.lane_change_delay = 10
            elif pressed_keys[pygame.K_RIGHT] and self.lane < LANES - 1:
                self.lane += 1
                self.set_lane_position()
                self.lane_change_delay = 10
        
        # Keep within bounds
        self.rect.clamp_ip(DISPLAY.get_rect())
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.shield_active:
            pygame.draw.circle(surface, (0, 100, 255), self.rect.center, 50, 2)


#enemies
class enemies(pygame.sprite.Sprite):
    def __init__(self, speed=None):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (LANE_WIDTH - 10, 50))
        self.rect = self.image.get_rect()
        self.lane = random.randint(0, LANES - 1)
        self.rect.centerx = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.rect.y = -50
        self.speed = speed or (BASE_SPEED * DIFFICULTY_MULTIPLIER)
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT


# ============= OBSTACLE CLASS =============
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type="pothole"):
        super().__init__()
        self.obstacle_type = obstacle_type
        self.create_obstacle()
        self.lane = random.randint(0, LANES - 1)
        self.rect.centerx = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.rect.y = -40
        self.speed = BASE_SPEED * DIFFICULTY_MULTIPLIER + 1
    
    def create_obstacle(self):
        """Create obstacle with different visual styles"""
        size = (LANE_WIDTH - 15, 30)
        self.image = pygame.Surface(size)
        
        if self.obstacle_type == "pothole":
            self.image.fill((40, 40, 40))  # Dark gray
            pygame.draw.circle(self.image, (20, 20, 20), (size[0]//2, size[1]//2), 10)
        elif self.obstacle_type == "oil":
            self.image.fill((60, 60, 60))  # Gray with oil sheen
            pygame.draw.circle(self.image, (100, 100, 100), (size[0]//2, size[1]//2), 12)
        elif self.obstacle_type == "barrier":
            self.image.fill((255, 100, 0))  # Orange barrier
            pygame.draw.line(self.image, (255, 200, 0), (0, 0), (size[0], size[1]), 3)
            pygame.draw.line(self.image, (255, 200, 0), (0, size[1]), (size[0], 0), 3)
        
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT


# ============= BOOST PAD CLASS =============
class BoostPad(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((LANE_WIDTH - 10, 40))
        self.image.fill((255, 215, 0))  # Gold color
        pygame.draw.circle(self.image, (255, 255, 0), (self.image.get_width()//2, self.image.get_height()//2), 8)
        self.rect = self.image.get_rect()
        self.lane = random.randint(0, LANES - 1)
        self.rect.centerx = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.rect.y = -40
        self.speed = BASE_SPEED * DIFFICULTY_MULTIPLIER
        self.boost_value = 2
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT


#coins
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(coin_img, (20, 20))
        self.rect = self.image.get_rect()
        self.lane = random.randint(0, LANES - 1)
        self.rect.centerx = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.rect.y = -20
        self.value = random.randint(5, 15)
    
    def update(self):
        self.rect.y += BASE_SPEED * DIFFICULTY_MULTIPLIER + 2
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT


# ============= GAME SETUP =============
# Game states
STATE_MAIN_MENU = 0
STATE_USERNAME = 1
STATE_PLAYING = 2
STATE_GAME_OVER = 3
STATE_LEADERBOARD = 4
STATE_SETTINGS = 5

current_state = STATE_MAIN_MENU
username = "Anonymous"

# Menu buttons
menu_buttons = [
    Button(50, 150, 300, 60, "PLAY"),
    Button(50, 230, 300, 60, "LEADERBOARD"),
    Button(50, 310, 300, 60, "SETTINGS"),
    Button(50, 390, 300, 60, "QUIT")
]

# Game variables
player = None
all_sprites = None
traffic_cars = None
obstacles = None
powerups = None
coins = None
start_btn = None

spawn_timer = 0
spawn_interval = 60
coin_timer = 0

def init_game():
    global player, all_sprites, traffic_cars, obstacles, powerups, coins, spawn_timer, spawn_interval, coin_timer, SCORE, COIN_SCORE, DIFFICULTY_MULTIPLIER
    
    SCORE = 0
    COIN_SCORE = 0
    DIFFICULTY_MULTIPLIER = 1.0
    
    player = Player()
    all_sprites = pygame.sprite.Group()
    traffic_cars = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    
    all_sprites.add(player)
    
    coin = Coin()
    coins.add(coin)
    all_sprites.add(coin)
    
    spawn_timer = 0
    spawn_interval = 60
    coin_timer = 0
    
    if background_sound:
        background_sound.play(-1)

# ============= MAIN GAME LOOP =============
running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and current_state != STATE_MAIN_MENU:
                current_state = STATE_MAIN_MENU
            
            # Username entry
            if current_state == STATE_USERNAME:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username.strip():
                        init_game()
                        current_state = STATE_PLAYING
                elif len(username) < 15 and event.unicode.isalnum():
                    username += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Username entry
            if current_state == STATE_USERNAME:
                if pygame.Rect(50, 300, 300, 50).collidepoint(mouse_pos):
                    if username.strip():
                        init_game()
                        current_state = STATE_PLAYING
            
            # Main menu
            if current_state == STATE_MAIN_MENU:
                for i, btn in enumerate(menu_buttons):
                    if btn.is_clicked(mouse_pos):
                        if i == 0:  # PLAY
                            username = "Anonymous"
                            current_state = STATE_USERNAME
                        elif i == 1:  # LEADERBOARD
                            current_state = STATE_LEADERBOARD
                        elif i == 2:  # SETTINGS
                            current_state = STATE_SETTINGS
                        elif i == 3:  # QUIT
                            running = False
            
            # Game over
            if current_state == STATE_GAME_OVER:
                # Retry button
                if pygame.Rect(50, 350, 300, 50).collidepoint(mouse_pos):
                    init_game()
                    current_state = STATE_PLAYING
                # Main menu button
                elif pygame.Rect(50, 420, 300, 50).collidepoint(mouse_pos):
                    if background_sound:
                        background_sound.stop()
                    current_state = STATE_MAIN_MENU
            
            # Leaderboard
            if current_state == STATE_LEADERBOARD:
                if pygame.Rect(50, 500, 300, 50).collidepoint(mouse_pos):
                    current_state = STATE_MAIN_MENU
            
            # Settings
            if current_state == STATE_SETTINGS:
                # Music toggle
                if pygame.Rect(250, 110, 100, 40).collidepoint(mouse_pos):
                    settings["music_enabled"] = not settings["music_enabled"]
                    update_audio_settings()
                    save_settings(settings)
                # Music volume down
                elif pygame.Rect(200, 160, 40, 30).collidepoint(mouse_pos):
                    settings["music_volume"] = max(0.0, settings["music_volume"] - 0.1)
                    update_audio_settings()
                    save_settings(settings)
                # Music volume up
                elif pygame.Rect(310, 160, 40, 30).collidepoint(mouse_pos):
                    settings["music_volume"] = min(1.0, settings["music_volume"] + 0.1)
                    update_audio_settings()
                    save_settings(settings)
                # Sound toggle
                elif pygame.Rect(250, 210, 100, 40).collidepoint(mouse_pos):
                    settings["sound_enabled"] = not settings["sound_enabled"]
                    update_audio_settings()
                    save_settings(settings)
                # Sound volume down
                elif pygame.Rect(200, 260, 40, 30).collidepoint(mouse_pos):
                    settings["sound_volume"] = max(0.0, settings["sound_volume"] - 0.1)
                    update_audio_settings()
                    save_settings(settings)
                # Sound volume up
                elif pygame.Rect(310, 260, 40, 30).collidepoint(mouse_pos):
                    settings["sound_volume"] = min(1.0, settings["sound_volume"] + 0.1)
                    update_audio_settings()
                    save_settings(settings)
                # Back to menu
                elif pygame.Rect(50, 500, 300, 50).collidepoint(mouse_pos):
                    current_state = STATE_MAIN_MENU
    
    # Update button hovers
    if current_state == STATE_MAIN_MENU:
        for btn in menu_buttons:
            btn.update(mouse_pos)
    
    # Main Menu
    if current_state == STATE_MAIN_MENU:
        DISPLAY.fill((0, 0, 0))
        title = font_huge.render("RACER GAME", True, (255, 215, 0))
        DISPLAY.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))
        
        for btn in menu_buttons:
            btn.draw(DISPLAY)
    
    # Username Entry
    elif current_state == STATE_USERNAME:
        DISPLAY.fill((0, 0, 0))
        title = font_large.render("ENTER YOUR NAME", True, (255, 215, 0))
        DISPLAY.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        input_box = pygame.Rect(50, 200, 300, 50)
        pygame.draw.rect(DISPLAY, (255, 255, 255), input_box, 2)
        
        username_text = font_medium.render(username + "_", True, (255, 255, 255))
        DISPLAY.blit(username_text, (input_box.x + 10, input_box.y + 10))
        
        start_btn = Button(50, 300, 300, 50, "START GAME")
        start_btn.update(mouse_pos)
        start_btn.draw(DISPLAY)
    
    # Leaderboard
    elif current_state == STATE_LEADERBOARD:
        DISPLAY.fill((0, 0, 0))
        title = font_huge.render("LEADERBOARD", True, (255, 215, 0))
        DISPLAY.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))
        
        try:
            if os.path.exists(LEADERBOARD_FILE):
                with open(LEADERBOARD_FILE, 'r') as f:
                    leaderboard = json.load(f)
            else:
                leaderboard = []
            
            y_pos = 120
            for i, entry in enumerate(leaderboard[:10]):
                rank_text = font_medium.render(f"{i+1}. {entry['name']}", True, (255, 255, 255))
                score_text = font_medium.render(f"Score: {entry['score']}", True, (200, 200, 200))
                date_text = font_small.render(f"{entry['date']}", True, (150, 150, 150))
                
                DISPLAY.blit(rank_text, (50, y_pos))
                DISPLAY.blit(score_text, (250, y_pos))
                DISPLAY.blit(date_text, (50, y_pos + 25))
                y_pos += 60
        except:
            no_data_text = font_medium.render("No leaderboard data", True, (200, 200, 200))
            DISPLAY.blit(no_data_text, (SCREEN_WIDTH//2 - no_data_text.get_width()//2, 200))
        
        back_btn = Button(50, 500, 300, 50, "BACK TO MENU")
        back_btn.draw(DISPLAY)
    
    # Settings
    elif current_state == STATE_SETTINGS:
        DISPLAY.fill((0, 0, 0))
        title = font_huge.render("SETTINGS", True, (255, 215, 0))
        DISPLAY.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))
        
        # Music settings
        music_text = font_medium.render(f"Music: {'ON' if settings['music_enabled'] else 'OFF'}", True, (255, 255, 255))
        DISPLAY.blit(music_text, (50, 120))
        
        music_toggle_btn = Button(250, 110, 100, 40, "TOGGLE")
        music_toggle_btn.draw(DISPLAY)
        
        music_vol_text = font_small.render(f"Volume: {int(settings['music_volume'] * 100)}%", True, (200, 200, 200))
        DISPLAY.blit(music_vol_text, (50, 170))
        
        music_vol_down_btn = Button(200, 160, 40, 30, "-")
        music_vol_up_btn = Button(310, 160, 40, 30, "+")
        music_vol_down_btn.draw(DISPLAY)
        music_vol_up_btn.draw(DISPLAY)
        
        # Sound settings
        sound_text = font_medium.render(f"Sound: {'ON' if settings['sound_enabled'] else 'OFF'}", True, (255, 255, 255))
        DISPLAY.blit(sound_text, (50, 220))
        
        sound_toggle_btn = Button(250, 210, 100, 40, "TOGGLE")
        sound_toggle_btn.draw(DISPLAY)
        
        sound_vol_text = font_small.render(f"Volume: {int(settings['sound_volume'] * 100)}%", True, (200, 200, 200))
        DISPLAY.blit(sound_vol_text, (50, 270))
        
        sound_vol_down_btn = Button(200, 260, 40, 30, "-")
        sound_vol_up_btn = Button(310, 260, 40, 30, "+")
        sound_vol_down_btn.draw(DISPLAY)
        sound_vol_up_btn.draw(DISPLAY)
        
        back_btn = Button(50, 500, 300, 50, "BACK TO MENU")
        back_btn.draw(DISPLAY)
    
    # Playing
    elif current_state == STATE_PLAYING:
        # Update difficulty based on score
        DIFFICULTY_MULTIPLIER = 1.0 + (SCORE // 10) * 0.15
        spawn_interval = max(30, 80 - int(SCORE // 5))
        
        # Update nitro timer
        if player.nitro_active:
            if pygame.time.get_ticks() - player.nitro_time > 5000:
                player.nitro_active = False
        
        # Spawn traffic cars
        spawn_timer += 1
        if spawn_timer > spawn_interval:
            traffic_car = enemies()
            all_sprites.add(traffic_car)
            traffic_cars.add(traffic_car)
            spawn_timer = 0
        
        # Spawn obstacles
        if random.random() < 0.015 * DIFFICULTY_MULTIPLIER:
            obstacle = Obstacle(random.choice(["pothole", "oil", "barrier"]))
            # Ensure safe spawn (not on player)
            while abs(obstacle.lane - player.lane) == 0:
                obstacle.lane = random.randint(0, LANES - 1)
                obstacle.rect.centerx = obstacle.lane * LANE_WIDTH + LANE_WIDTH // 2
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
        
        # Spawn boost pads
        if random.random() < 0.008:
            boost = BoostPad()
            # Ensure safe spawn (not on player)
            while boost.lane == player.lane:
                boost.lane = random.randint(0, LANES - 1)
                boost.rect.centerx = boost.lane * LANE_WIDTH + LANE_WIDTH // 2
            all_sprites.add(boost)
            powerups.add(boost)
        
        # Spawn power-ups (nitro, shield, repair)
        if random.random() < 0.005:
            power_type = random.choice(["nitro", "shield", "repair"])
            lane = random.randint(0, LANES - 1)
            # Ensure safe spawn (not on player)
            while lane == player.lane:
                lane = random.randint(0, LANES - 1)
            pu = PowerUp(lane, power_type)
            all_sprites.add(pu)
            powerups.add(pu)
        
        # Spawn coins
        coin_timer += 1
        if coin_timer > 120:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
            coin_timer = 0
        
        # Update all sprites
        for sprite in all_sprites:
            sprite.update()
        
        # Remove off-screen sprites and award points
        for car in traffic_cars:
            if car.is_off_screen():
                car.kill()
                SCORE += 1
        
        for obstacle in obstacles:
            if obstacle.is_off_screen():
                obstacle.kill()
        
        for boost in powerups:
            if boost.is_off_screen():
                boost.kill()
        
        for boost in list(powerups):
            if hasattr(boost, 'is_expired') and boost.is_expired():
                boost.kill()
        
        for coin_sprite in coins:
            if coin_sprite.is_off_screen():
                coin_sprite.kill()
        
        # Collision detection - Traffic cars (Game Over)
        for car in traffic_cars:
            if pygame.sprite.collide_rect(player, car):
                if player.shield_active:
                    player.shield_active = False
                    car.kill()
                else:
                    if crash_sound:
                        crash_sound.play()
                    current_state = STATE_GAME_OVER
        
        # Collision detection - Obstacles (Game Over)
        for obstacle in obstacles:
            if pygame.sprite.collide_rect(player, obstacle):
                if player.shield_active:
                    player.shield_active = False
                    obstacle.kill()
                else:
                    if crash_sound:
                        crash_sound.play()
                    current_state = STATE_GAME_OVER
        
        # Collision detection - Coins
        for coin_sprite in coins:
            if pygame.sprite.collide_rect(player, coin_sprite):
                COIN_SCORE += coin_sprite.value
                coin_sprite.kill()
        
        # Collision detection - Power-ups
        for boost in list(powerups):
            if pygame.sprite.collide_rect(player, boost):
                if isinstance(boost, PowerUp):
                    if boost.power_type == "nitro":
                        player.nitro_active = True
                        player.nitro_time = pygame.time.get_ticks()
                        COIN_SCORE += 50
                    elif boost.power_type == "shield":
                        player.shield_active = True
                        COIN_SCORE += 50
                    elif boost.power_type == "repair":
                        COIN_SCORE += 100
                    boost.kill()
                elif isinstance(boost, BoostPad):
                    COIN_SCORE += 50
                    boost.kill()
        
        # Draw everything
        DISPLAY.blit(background_img, (0, 0))
        
        # Draw lane separators
        for i in range(1, LANES):
            x = i * LANE_WIDTH
            pygame.draw.line(DISPLAY, (255, 255, 255), (x, 0), (x, SCREEN_HEIGHT), 2)
        
        # Draw all sprites
        for sprite in all_sprites:
            sprite.draw(DISPLAY)
        
        # Draw HUD
        score_text = font_large.render(f"Distance: {SCORE}", True, (255, 255, 255))
        DISPLAY.blit(score_text, (10, 10))
        
        coin_text = font_medium.render(f"Coins: {COIN_SCORE}", True, (255, 215, 0))
        DISPLAY.blit(coin_text, (SCREEN_WIDTH - 150, 10))
        
        difficulty_text = font_small.render(f"Speed: {DIFFICULTY_MULTIPLIER:.1f}x", True, (200, 200, 200))
        DISPLAY.blit(difficulty_text, (10, 50))
        
        # Power-up indicators
        if player.nitro_active:
            nitro_time_left = max(0, 5 - (pygame.time.get_ticks() - player.nitro_time) // 1000)
            nitro_text = font_small.render(f"NITRO: {nitro_time_left}s", True, (255, 255, 0))
            DISPLAY.blit(nitro_text, (SCREEN_WIDTH - 120, 35))
        
        if player.shield_active:
            shield_text = font_small.render("SHIELD: ON", True, (0, 100, 255))
            DISPLAY.blit(shield_text, (SCREEN_WIDTH - 120, 55))
    
    # Game Over
    elif current_state == STATE_GAME_OVER:
        DISPLAY.fill((0, 0, 0))
        game_over_text = font_large.render("GAME OVER!", True, (255, 0, 0))
        final_score_text = font_medium.render(f"Score: {SCORE + COIN_SCORE}", True, (255, 255, 255))
        final_distance_text = font_medium.render(f"Distance: {SCORE}", True, (255, 255, 255))
        final_coins_text = font_medium.render(f"Coins: {COIN_SCORE}", True, (255, 215, 0))
        
        DISPLAY.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 50))
        DISPLAY.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, 140))
        DISPLAY.blit(final_distance_text, (SCREEN_WIDTH//2 - final_distance_text.get_width()//2, 190))
        DISPLAY.blit(final_coins_text, (SCREEN_WIDTH//2 - final_coins_text.get_width()//2, 240))
        
        # Save score to leaderboard
        save_score(username, SCORE + COIN_SCORE, SCORE, COIN_SCORE)
        
        # Buttons
        retry_btn = Button(50, 350, 300, 50, "RETRY")
        menu_btn = Button(50, 420, 300, 50, "MAIN MENU")
        retry_btn.draw(DISPLAY)
        menu_btn.draw(DISPLAY)
    
    pygame.display.update()
    clock.tick(60)

if background_sound:
    background_sound.stop()

pygame.quit()