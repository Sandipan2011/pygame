import pygame
import random
import os
from config import WIDTH, HEIGHT, CAR_COLOR, BG_COLOR, FPS, Difficulty
from config import DIFFICULTY_SETTINGS, CRASH_SOUND, SCORE_SOUND
from config import ENGINE_SOUND, POWERUP_SOUND
from game_utils import create_obstacle, create_power_up


# Initialize
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()


# Load assets
def load_image(name):
    path = os.path.join('assets', name)
    try:
        image = pygame.image.load(path)
        return image
    except Exception:
        print(f"Warning: Could not load image {path}")
        # Fallback to colored rectangle
        surf = pygame.Surface((50, 100))
        surf.fill(CAR_COLOR if 'car' in name else (0, 255, 0))
        return surf


def load_sound(name):
    path = os.path.join('assets', name)
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except Exception:
        print(f"Warning: Could not load sound {path}")
        return None


# Load images and sounds
crash_sound = load_sound(CRASH_SOUND)
score_sound = load_sound(SCORE_SOUND)
engine_sound = load_sound(ENGINE_SOUND)
powerup_sound = load_sound(POWERUP_SOUND)
car_image = load_image('car.png')
obstacle_image = load_image('car.png')  # Same image for obstacles

# Scale images if needed
car_image = pygame.transform.scale(car_image, (50, 100))
obstacle_image = pygame.transform.scale(obstacle_image, (50, 100))

car_rect = car_image.get_rect(center=(WIDTH // 2, HEIGHT - 120))


# Game state
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2


current_state = GameState.MENU
score = 0
high_score = 0
current_difficulty = Difficulty.MEDIUM  # Default difficulty

# Road lines
line_height = 20
lines = [(WIDTH // 2 - 5, y) for y in range(0, HEIGHT, 40)]

# Power-ups
power_ups = []
active_power_up = None
power_up_timer = 0

# Fonts
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)


def reset_game():
    global car_rect, obstacles, score, lines, current_state
    car_rect.center = (WIDTH // 2, HEIGHT - 120)
    obstacles = []
    score = 0
    lines = [(WIDTH // 2 - 5, y) for y in range(0, HEIGHT, 40)]
    current_state = GameState.PLAYING


def draw_menu():
    screen.fill(BG_COLOR)
    title = font_large.render("CAR RACING", True, (255, 255, 255))
    instruction = font_medium.render(
        "Press SPACE to start", True, (255, 255, 255))
    difficulty_text = font_medium.render(
        f"Difficulty: {DIFFICULTY_SETTINGS[current_difficulty]['name']}", 
        True, (255, 255, 255))
    change_text = font_small.render(
        "Press 1-3 to change difficulty", True, (200, 200, 200))
    high_score_text = font_small.render(
        f"High Score: {high_score}", True, (255, 255, 255))
    
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
    screen.blit(instruction, 
                (WIDTH//2 - instruction.get_width()//2, HEIGHT//2))
    screen.blit(difficulty_text, 
                (WIDTH//2 - difficulty_text.get_width()//2, HEIGHT//2 + 40))
    screen.blit(change_text, 
                (WIDTH//2 - change_text.get_width()//2, HEIGHT//2 + 80))
    screen.blit(high_score_text, 
                (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 120))


def draw_game_over():
    screen.fill(BG_COLOR)
    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    score_text = font_medium.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font_medium.render(
        f"High Score: {high_score}", True, (255, 255, 255))
    restart_text = font_small.render(
        "Press R to restart", True, (255, 255, 255))
    
    screen.blit(game_over_text, 
                (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
    screen.blit(score_text, 
                (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(high_score_text, 
                (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 50))
    screen.blit(restart_text, 
                (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 100))


def draw_playing():
    global lines, score, current_state, high_score
    screen.fill(BG_COLOR)

    # Draw road lines
    new_lines = []
    for x, y in lines:
        y += 10
        if y > HEIGHT:
            y = 0
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 10, line_height))
        new_lines.append((x, y))
    lines = new_lines

    # Draw obstacles
    settings = DIFFICULTY_SETTINGS[current_difficulty]
    obstacle_speed = settings['obstacle_speed']
    
    for obs in obstacles[:]:
        obs.y += obstacle_speed
        screen.blit(obstacle_image, obs)
        if obs.y > HEIGHT:
            obstacles.remove(obs)
            score += 1
            if score_sound:
                score_sound.play()
        if car_rect.colliderect(obs):
            if crash_sound:
                crash_sound.play()
            current_state = GameState.GAME_OVER
            high_score = max(high_score, score)

    # Draw power-ups
    for power_up in power_ups:
        if power_up['type'] == 'speed':
            color = (255, 165, 0)  # Orange for speed
        elif power_up['type'] == 'shield':
            color = (0, 0, 255)    # Blue for shield
        elif power_up['type'] == 'score_multiplier':
            color = (255, 255, 0)  # Yellow for score multiplier
        else:
            color = (255, 0, 255)  # Magenta as fallback
        pygame.draw.rect(screen, color, power_up['rect'])

    # Draw car
    screen.blit(car_image, car_rect)

    # Draw score
    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if current_state == GameState.MENU:
                if event.key == pygame.K_SPACE:
                    reset_game()
                elif event.key == pygame.K_1:
                    current_difficulty = Difficulty.EASY
                elif event.key == pygame.K_2:
                    current_difficulty = Difficulty.MEDIUM
                elif event.key == pygame.K_3:
                    current_difficulty = Difficulty.HARD
            elif (current_state == GameState.GAME_OVER and 
                  event.key == pygame.K_r):
                reset_game()

    if current_state == GameState.MENU:
        draw_menu()
    elif current_state == GameState.PLAYING:
        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_rect.left > 0:
            car_rect.x -= 5
        if keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
            car_rect.x += 5
        
        # Generate obstacles based on difficulty
        settings = DIFFICULTY_SETTINGS[current_difficulty]
        obstacle_frequency = settings['obstacle_frequency']
        if random.randint(1, obstacle_frequency) == 1:
            obstacles.append(create_obstacle(WIDTH))
        
        # Power-up generation logic
        if random.randint(1, 100) <= 5:  # 5% chance to spawn a power-up
            power_ups.append(create_power_up(WIDTH))
        
        # Update power-ups
        for power_up in power_ups[:]:
            power_up['rect'].y += 5  # Move power-up down
            if power_up['rect'].y > HEIGHT:
                power_ups.remove(power_up)  # Remove off-screen power-ups
            if car_rect.colliderect(power_up['rect']):
                # Apply power-up effect
                active_power_up = power_up['type']
                power_up_timer = power_up['duration']
                print(f"Collected {active_power_up} power-up!")
                if powerup_sound:
                    powerup_sound.play()
                power_ups.remove(power_up)  # Remove collected power-up

        # Handle active power-up effects
        if active_power_up:
            power_up_timer -= clock.get_time()
            if power_up_timer <= 0:
                print(f"{active_power_up} power-up expired!")
                active_power_up = None  # Reset power-up
        
        draw_playing()
    elif current_state == GameState.GAME_OVER:
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
