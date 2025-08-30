# Game Settings

# Sound settings (files may not exist - game handles missing sounds gracefully)
CRASH_SOUND = 'crash.wav'
SCORE_SOUND = 'score.wav'
ENGINE_SOUND = 'engine.wav'
POWERUP_SOUND = 'powerup.wav'

# Screen size
WIDTH = 800
HEIGHT = 600

# Colors
CAR_COLOR = (255, 0, 0)      # Red
OBSTACLE_COLOR = (0, 255, 0)  # Green
BG_COLOR = (50, 50, 50)      # Dark Gray
LINE_COLOR = (255, 255, 255)  # White

# Car settings
CAR_WIDTH = 50
CAR_HEIGHT = 100

# Obstacle settings
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 100
OBSTACLE_SPEED = 7

# Game speed
FPS = 60


# Difficulty settings
class Difficulty:
    EASY = 0
    MEDIUM = 1
    HARD = 2


# Difficulty parameters
DIFFICULTY_SETTINGS = {
    Difficulty.EASY: {
        'obstacle_speed': 5,
        'obstacle_frequency': 80,  # Higher number = less frequent
        'line_speed': 8,
        'name': 'EASY'
    },
    Difficulty.MEDIUM: {
        'obstacle_speed': 7,
        'obstacle_frequency': 60,
        'line_speed': 10,
        'name': 'MEDIUM'
    },
    Difficulty.HARD: {
        'obstacle_speed': 9,
        'obstacle_frequency': 40,
        'line_speed': 12,
        'name': 'HARD'
    }
}
