import pygame
import sys

# Initialize Pygame
pygame.init()

# Set screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Display")

# Set up clock
clock = pygame.time.Clock()

# Load car image (your uploaded file)
car_image = pygame.image.load(
    "vecteezy_png-3d-rendering-illustration-blank-cut-out-mockup_25308136.png")
car_image = pygame.transform.scale(car_image, (60, 120))  # Resize if needed

# Initial car position
car_x = SCREEN_WIDTH // 2 - 30
car_y = SCREEN_HEIGHT - 150

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen with black

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw car
    screen.blit(car_image, (car_x, car_y))

    # Update screen
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
