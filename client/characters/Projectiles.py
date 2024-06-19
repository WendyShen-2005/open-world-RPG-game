import os.path

import pygame


class Projectile(pygame.sprite.Sprite):

    mouse_pos = (-100, -100)

    def __init__(self, starting_pos, group):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join('client', 'characters', 'bullet1.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=starting_pos)
        self.speed = 3
        print(str(starting_pos) + " " + str(Projectile.mouse_pos))
        self.direction = (pygame.math.Vector2(Projectile.mouse_pos[0], Projectile.mouse_pos[1]) -
                          pygame.math.Vector2(starting_pos[0], starting_pos[1]))
        # print(str(self.direction))

        self.direction = self.direction.normalize()

    def update(self):
        self.rect.center += self.direction * self.speed
