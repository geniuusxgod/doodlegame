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
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = -10
            self.jumping = True
        else:
            self.jumping = True

    def reset_position(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - self.rect.height - 10
        self.velocity_y = 0

    def check_bounds(self):
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.x + self.rect.width > WIDTH:
            self.rect.x = -self.rect.width

    def update(self, keys):
        self.move(keys)
        self.apply_gravity()
        self.check_bounds()
        self.update_images()

    def check_collision(self, platforms):
        """
        Проверка столкновений с платформами.
        """
        for platform in platforms:
            # Проверяем, чтобы игрок касался только верхней части платформы
            if (
                    self.rect.bottom >= platform.rect.top and  # Нижняя часть игрока касается верхней платформы
                    self.rect.bottom <= platform.rect.top + 10 and  # Допустимый допуск для столкновения
                    self.rect.right > platform.rect.left and  # Игрок пересекает платформу по X
                    self.rect.left < platform.rect.right and
                    self.velocity_y > 0  # Игрок должен падать вниз
            ):
                self.rect.bottom = platform.rect.top  # Ставим игрока на платформу
                self.velocity_y = -10  # Задаём импульс вверх
                self.jumping = True
                break

