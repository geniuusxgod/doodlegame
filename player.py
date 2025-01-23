import os

from settings import *

class Player:
    def __init__(self, position):
        self.frames = {'left': [], 'right': [], 'batut': [], 'pruzhini': [], 'elitri': []}
        self.load_images()
        self.state, self.frame_index = 'right', 0
        self.image = self.frames[self.state][0] if self.frames[self.state] else None
        self.rect = pygame.Rect(position[0], position[1], 50, 50)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.3

    def load_images(self):
        pass

    def move(self, keys):
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.rect.x += self.direction.x * self.speed

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = -10

    def reset_position(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - self.rect.height - 10
        self.velocity_y = 0

    def check_bounds(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.width > WIDTH:
            self.rect.x = WIDTH - self.rect.width

    def update(self, keys):
        self.move(keys)
        self.apply_gravity()
        self.check_bounds()
