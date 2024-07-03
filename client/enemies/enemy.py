import abc

import pygame.sprite


class Enemy(abc.ABC, pygame.sprite.Sprite):
    @abc.abstractmethod
    def __init__(self, startingX, startingY, img, speed):
        super.__init__()  # pygame sprite vars
        self.x = startingX
        self.y = startingY
        self.targetX = startingX
        self.targetY = startingY
        self.moves = []
        self.speed = speed

    def set_target_location():
        # find a location that is between 700-500px away from here
        # set targetX and targetY to that coordinate
        pass

    def find_path(self):
        pass
        # find a way to that to that location

    def move(self, direction):
        match direction:
            case "up": self.y -= self.speed
            case "down": self.y += self.speed
            case "right": self.x += self.speed
            case "left": self.x -= self.speed
