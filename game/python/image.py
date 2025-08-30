import pygame
pygame.init()
car_image = pygame.image.load("car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (50, 50))
