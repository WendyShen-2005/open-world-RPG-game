import os.path

import pygame


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join('client', 'environment', 'tree.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.actual_height = 0.3
