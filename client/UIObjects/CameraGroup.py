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
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2

        # controls how zoomed in we are
        self.zoom_scale = 1

        # 
        self.internal_surface_size = (2500,2500)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)

        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0]//2 - self.half_w
        self.internal_offset.y = self.internal_surface_size[1]//2 - self.half_h

    def zoom_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and self.zoom_scale < 1.55:
            self.zoom_scale += 0.05
        elif keys[pygame.K_e] and self.zoom_scale > 0.45:
            self.zoom_scale -= 0.05

    def set_offset(self, x, y):
        self.offset = pygame.math.Vector2(x, y)

    def custom_draw(self):
        self.internal_surface.fill('#a9d0db')
        ground_offset = self.ground_rect.topleft + self.offset + self.internal_offset
        self.internal_surface.blit(self.ground_surf, ground_offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft + self.offset + self.internal_offset
            self.internal_surface.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)
