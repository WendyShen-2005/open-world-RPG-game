import pygame


class PlayableChar:

    def __init__(self, starting_x, starting_y, speed, height, width):
        self.x = starting_x
        self.y = starting_y
        self.speed = speed
        self.height = height
        self.width = width

    def display(self, screen):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))