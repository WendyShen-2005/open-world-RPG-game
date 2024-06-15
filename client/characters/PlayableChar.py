import os.path

import pygame


class PlayableChar(pygame.sprite.Sprite):  # using the pygame.sprite.Sprite super class

    def __init__(self, starting_x, starting_y, group):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join('client', 'characters', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(starting_x, starting_y))
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def set_pos(self, x, y):
        self.rect.center = pygame.math.Vector2(x, y)

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed