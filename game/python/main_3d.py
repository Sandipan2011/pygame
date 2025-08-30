import pygame
import random
import os
import math
from config import WIDTH, HEIGHT, CAR_COLOR, FPS, Difficulty
from config import DIFFICULTY_SETTINGS, CRASH_SOUND, SCORE_SOUND
from config import ENGINE_SOUND, POWERUP_SOUND
from game_utils import create_power_up
from render_3d import Renderer3D
from config_3d import ROAD_WIDTH, TRACK_LENGTH


# Initialize
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asphalt Legends - 3D Racing")
clock = pygame.time.Clock()

# Initialize 3D renderer
renderer = Renderer3D(WIDTH, HEIGHT)
renderer.create_road_segments(TRACK_LENGTH)

# Load assets
def load_image(name):
    path = os.path.join('game', 'python', 'assets', name)
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
    path = os.path.join('game', 'python', 'assets', name)
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

# Game state
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2


current_state = GameState.MENU
score = 0
high_score = 0
current_difficulty = Difficulty.MEDIUM  # Default difficulty

# Player car properties
player_x = 0  # X position in 3D space (-ROAD_WIDTH/2 to ROAD_WIDTH/2)
player_z = 0  # Z position (progress along track)
player_speed = 0
max_speed = 20
acceleration = 0.2
deceleration = 0.1

# Road lines and obstacles will be handled in 3D space
obstacles = []
power_ups = []
active_power_up = None
power_up_timer = 0

# Fonts
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)


def reset_game():
    global player_x, player_z, player_speed, obstacles, power_ups
    global score, current_state, active_power_up, power_up_timer
    
    player_x = 0
    player_z = 0
    player_speed = 5  # Start with some speed
    obstacles = []
    power_ups = []
    active_power_up = None
    power_up_timer = 0
    score = 0
    current_state = GameState.PLAYING
    renderer.create_road_segments(TRACK_LENGTH)


def draw_menu():
    screen.fill((0, 0, 0))
    title = font_large.render("ASPHALT LEGENDS", True, (255, 255, 255))
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
    screen.fill((0, 0, 0))
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


def update_gameplay():
    global player_x, player_z, player_speed, score, current_state, high_score
    global active_power_up, power_up_timer
    
    # Update player position based on speed
    player_z += player_speed
    
    # Handle controls
    keys = pygame.key.get_pressed()
    
    # Acceleration/braking
    if keys[pygame.K_UP]:
        player_speed = min(player_speed + acceleration, max_speed)
    elif keys[pygame.K_DOWN]:
        player_speed = max(player_speed - deceleration * 2, 0)
    else:
        # Natural deceleration
        player_speed = max(player_speed - deceleration, 0)
    
    # Steering
    steering_speed = 0.5
    if keys[pygame.K_LEFT]:
        player_x = max(player_x - steering_speed, -ROAD_WIDTH/2)
    if keys[pygame.K_RIGHT]:
        player_x = min(player_x + steering_speed, ROAD_WIDTH/2)
    
    # Update camera to follow player
    renderer.update_camera(player_x, player_z, player_speed)
    
    # Generate obstacles based on difficulty
    settings = DIFFICULTY_SETTINGS[current_difficulty]
    obstacle_frequency = settings['obstacle_frequency']
    
    if random.randint(1, obstacle_frequency) == 1:
        obstacle_x = random.randint(-int(ROAD_WIDTH/2), int(ROAD_WIDTH/2))
        obstacle_z = player_z + 2000  # Spawn ahead of player
        obstacles.append({
            'x': obstacle_x,
            'z': obstacle_z,
            'width': 100,
            'height': 50
        })
    
    # Power-up generation logic
    if random.randint(1, 100) <= 5:  # 5% chance to spawn a power-up
        power_up_x = random.randint(-int(ROAD_WIDTH/2), int(ROAD_WIDTH/2))
        power_up_z = player_z + 1500  # Spawn ahead of player
        power_ups.append(create_power_up(power_up_x, power_up_z))
    
    # Update obstacles and check collisions
    for obstacle in obstacles[:]:
        obstacle['z'] -= player_speed
        
        # Check if obstacle is behind player
        if obstacle['z'] < player_z - 100:
            obstacles.remove(obstacle)
            score += 1
            if score_sound:
                score_sound.play()
        
        # Check collision
        distance = math.sqrt((obstacle['x'] - player_x)**2 + 
                             (obstacle['z'] - player_z)**2)
        if distance < 100:  # Collision threshold
            if crash_sound:
                crash_sound.play()
            current_state = GameState.GAME_OVER
            high_score = max(high_score, score)
    
    # Update power-ups
    for power_up in power_ups[:]:
        power_up['z'] -= player_speed
        
        # Remove off-screen power-ups
        if power_up['z'] < player_z - 100:
            power_ups.remove(power_up)
        
        # Check power-up collection
        distance = math.sqrt(
            (power_up['x'] - player_x)**2 + (power_up['z'] - player_z)**2
        )
        if distance < 80:  # Collection threshold
            active_power_up = power_up['type']
            power_up_timer = power_up['duration']
            print(f"Collected {active_power_up} power-up!")
            if powerup_sound:
                powerup_sound.play()
            power_ups.remove(power_up)
    
    # Handle active power-up effects
    if active_power_up:
        power_up_timer -= clock.get_time()
        if power_up_timer <= 0:
            print(f"{active_power_up} power-up expired!")
            active_power_up = None


def draw_playing():
    # Render 3D scene
    renderer.render_sky_and_ground(screen)
    renderer.render_road(screen)
    
    # Render obstacles
    for obstacle in obstacles:
        # Simple obstacle rendering - will be improved later
        screen_x, screen_y, scale = renderer.project(
            obstacle['x'], 0, obstacle['z'] - renderer.camera_z,
            renderer.camera_x, renderer.camera_y, renderer.camera_z
        )
        if scale > 0.01:
            obstacle_width = obstacle['width'] * scale
            obstacle_height = obstacle['height'] * scale
            pygame.draw.rect(
                screen, (255, 0, 0),
                (screen_x - obstacle_width/2, screen_y - obstacle_height/2,
                 obstacle_width, obstacle_height)
            )
    
    # Render power-ups
    for power_up in power_ups:
        screen_x, screen_y, scale = renderer.project(
            power_up['x'], 0, power_up['z'] - renderer.camera_z,
            renderer.camera_x, renderer.camera_y, renderer.camera_z
        )
        if scale > 0.01:
            if power_up['type'] == 'speed':
                color = (255, 165, 0)  # Orange
            elif power_up['type'] == 'shield':
                color = (0, 0, 255)    # Blue
            elif power_up['type'] == 'score_multiplier':
                color = (255, 255, 0)  # Yellow
            else:
                color = (255, 0, 255)  # Magenta
            
            power_up_size = 30 * scale
            pygame.draw.rect(
                screen, color,
                (screen_x - power_up_size/2, screen_y - power_up_size/2,
                 power_up_size, power_up_size)
            )
    
    # Render player car
    renderer.render_car(screen, player_x, player_z, car_image)
    
    # Draw HUD
    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    speed_text = font_small.render(f"Speed: {int(player_speed * 10)} km/h", True, (255, 255, 255))
    
    screen.blit(score_text, (10, 10))
    screen.blit(speed_text, (10, 40))
    
    # Show active power-up
    if active_power_up:
        power_up_text = font_small.render(
            f"Power-up: {active_power_up} ("
            f"{int(power_up_timer/1000)}s)", 
            True, (255, 255, 255)
        )
        screen.blit(power_up_text, (10, 70))


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
        update_gameplay()
        draw_playing()
    elif current_state == GameState.GAME_OVER:
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
