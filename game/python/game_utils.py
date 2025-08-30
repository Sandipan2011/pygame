import random
import pygame


def create_obstacle(screen_width, width=50, height=100):
    """
    Create a new obstacle at a random x-position in 2D space.
    """
    x = random.randint(0, screen_width - width)
    obstacle_type = random.choice(['normal', 'zigzag', 'slow'])
    zigzag_dir = random.choice([-1, 1]) if obstacle_type == 'zigzag' else 0
    speed_mult = 0.5 if obstacle_type == 'slow' else 1.0
    obstacle = {
        'rect': pygame.Rect(x, -height, width, height),
        'type': obstacle_type,
        'zigzag_direction': zigzag_dir,
        'speed_multiplier': speed_mult
    }
    return obstacle


def create_power_up(screen_width, width=30, height=30):
    """
    Create a new power-up in 2D space.
    """
    x = random.randint(0, screen_width - width)
    power_up_types = [
        'speed', 'shield', 'score_multiplier', 
        'invincibility', 'slow_motion'
    ]
    power_up = {
        'rect': pygame.Rect(x, -height, width, height),
        'type': random.choice(power_up_types),
        'duration': 5000  # 5 seconds duration
    }
    return power_up
