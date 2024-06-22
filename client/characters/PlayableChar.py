import os.path

import pygame
from client.characters.Projectiles import Projectile
from client.UIObjects.MouseAttributes import MouseAttributes

class PlayableChar(pygame.sprite.Sprite, MouseAttributes):  # using the pygame.sprite.Sprite super class

    def __init__(self, starting_x, starting_y, group):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join('client', 'characters', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(starting_x, starting_y))
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.projectiles = []
        self.group = group

    def add_projectile(self, end_pos):
        new_proj = Projectile(self.rect.center, end_pos, self.group)
        self.projectiles.append(new_proj)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def set_pos(self, x, y):
        self.rect.center = pygame.math.Vector2(x, y)

    def get_pos(self):
        pos = str(self.rect.centerx) + " " + str(self.rect.centery)
        return pos

    def update(self):
        mouse_offset = pygame.math.Vector2(MouseAttributes.get_offset())
        base_pos = pygame.math.Vector2(MouseAttributes.get_mouse_pos())
        # print(str(mouse_offset) + " " + str(base_pos) + " hello :)")
        base_pos = base_pos - mouse_offset
        if MouseAttributes.get_mouse_click():
            self.add_projectile(base_pos)
        elif MouseAttributes.get_mouse_hold():
            upper_pos = base_pos.rotate(10)
            lower_pos = base_pos.rotate(-10)
            self.add_projectile(base_pos)
            self.add_projectile(upper_pos)
            self.add_projectile(lower_pos)


        self.input()
        self.rect.center += self.direction * self.speed

    # obstacle_actual_rect = percentage of obstacle height that's the actual height
    def collision_detection(self, obstacle_rect, obstacle_actual_height):
        c_right = self.rect.x + self.rect.width
        c_left = self.rect.x
        c_top = self.rect.y
        c_bottom = self.rect.y + self.rect.height

        w_right = obstacle_rect.x + obstacle_rect.width
        w_left = obstacle_rect.x
        w_top = obstacle_rect.y + obstacle_rect.height * (1-obstacle_actual_height)
        w_bottom = obstacle_rect.y + obstacle_rect.height

        if (c_right > w_left > c_left and
                c_right - w_left < c_bottom - w_top and
                c_right - w_left < w_bottom - c_top):  # collide with left side of wall
            self.rect.x = w_left - self.rect.width
        elif (c_left < w_right < c_right and
              w_right - c_left < c_bottom - w_top and
              w_right - c_left < w_bottom - c_top):  # collide with right side of wall
            self.rect.x = w_right
        elif (c_bottom > w_top > c_top and
              (c_right > w_left and c_left < w_right)):  # rect collides from top side of the wall
            self.rect.y = w_top - self.rect.height
        elif (c_top < w_bottom < c_bottom and
              (c_right > w_left and c_left < w_right)):  # rect collides from bottom side of the wall
            self.rect.y = w_bottom

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            self.collision_detection(obstacle.rect, obstacle.actual_height)
