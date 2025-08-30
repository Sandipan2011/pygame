import random
import pygame


def create_obstacle(screen_width, width=50, height=100):
    """
    Create a new obstacle at a random x-position in 2D space.
    """
    x = random.randint(0, screen_width - width)
    obstacle = pygame.Rect(x, -height, width, height)
    return obstacle


def create_power_up(screen_width, width=30, height=30):
    """
    Create a new power-up in 2D space.
    """
    x = random.randint(0, screen_width - width)
    power_up = {
        'rect': pygame.Rect(x, -height, width, height),
        'type': random.choice(['speed', 'shield', 'score_multiplier']),
        'duration': 5000  # 5 seconds duration
    }
    return power_up
