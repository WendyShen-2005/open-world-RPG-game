import os.path

import pygame

class camera_group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # ground
        self.ground_surf = pygame.image.load(os.path.join('client', 'environment', 'backgrounds', 'ground.png')).convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # camera offset
        self.offset = pygame.math.Vector2()

    def set_offset(self, x, y):
        self.offset = pygame.math.Vector2(x, y)
    def custom_draw(self):
        ground_offset = self.ground_rect.topleft + self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
