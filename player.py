import os

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.3


        self.direction = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(position[0], position[1], 50, 50)


        self.jumping = False
        self.left = False
        self.right = True

        self.right_image = pygame.image.load(join('assets', 'player', 'right.png')).convert_alpha()
        self.left_image = pygame.image.load(join('assets', 'player', 'left.png')).convert_alpha()
        self.right_jump_image = pygame.image.load(join('assets', 'player', 'right_jump.png')).convert_alpha()
        self.left_jump_image = pygame.image.load(join('assets', 'player', 'left_jump.png')).convert_alpha()

    def update_images(self):
        if not self.jumping:
            if self.right:
                self.image = self.right_image
            elif self.left:
                self.image = self.left_image
        elif self.jumping:
            if self.right:
                self.image = self.right_jump_image
            elif self.left:
                self.image = self.left_jump_image


    def move(self, keys):
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.rect.x += self.direction.x * self.speed

        if self.direction.x > 0:
            self.right = True
            self.left = False
        elif self.direction.x < 0:
            self.right = False
            self.left = True

    def apply_gravity(self):
        # Увеличиваем вертикальную скорость из-за гравитации
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Проверяем, находится ли игрок у края экрана
        if self.rect.bottom >= HEIGHT - 2:  # Допускаем небольшую погрешность
            self.rect.bottom = HEIGHT  # Выравниваем игрока по краю экрана
            self.velocity_y = -10  # Задаем скорость для прыжка
            self.jumping = True  # Игрок начинает новый прыжок
        else:
            self.jumping = True

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
        self.update_images()
