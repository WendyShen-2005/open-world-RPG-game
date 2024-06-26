import os.path

import pygame


class Projectile(pygame.sprite.Sprite):

    mouse_pos = (-100, -100)

    def __init__(self, starting_pos, end_pos, group):
        super().__init__(group)
        self.start = starting_pos
        self.end = end_pos

        self.image = pygame.image.load(os.path.join('client', 'characters', 'bullet1.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=starting_pos)
        self.speed = 3
        # print(str(starting_pos) + " " + str(Projectile.mouse_pos) + " " + str(end_pos))
        self.direction = (pygame.math.Vector2(end_pos[0], end_pos[1]) -
                          pygame.math.Vector2(starting_pos[0], starting_pos[1]))

        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        self.__timer = 0

    def get_start_and_end(self):
        return [self.rect.topleft, self.rect.topleft + self.direction]

    def get_timer(self):
        return self.__timer

    def update(self):
        self.__timer += 1
        self.rect.center += self.direction * self.speed
