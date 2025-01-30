import os

import pygame.image

from platforma import BrokenPlatform
from groups import AllSprites
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, all_sprites, bullets):
        super().__init__()
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.2

        self.direction = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(position[0], position[1], 50, 50)

        self.jumping = False
        self.left = False
        self.right = True
        self.shooting = False
        self.shooting_timer = 0

        self.all_sprites = all_sprites
        self.bullets = bullets

        self.right_image = pygame.image.load(join('assets', 'player', 'right.png')).convert_alpha()
        self.left_image = pygame.image.load(join('assets', 'player', 'left.png')).convert_alpha()
        self.right_jump_image = pygame.image.load(join('assets', 'player', 'right_jump.png')).convert_alpha()
        self.left_jump_image = pygame.image.load(join('assets', 'player', 'left_jump.png')).convert_alpha()
        self.shooting_image = pygame.image.load(join('assets', 'player', 'shoot.png')).convert_alpha()
        self.shooting_jump_image = pygame.image.load(join('assets', 'player', 'shoot_jump.png')).convert_alpha()

        self.image = self.right_image


    def update_images(self):
        if self.shooting:  # Приоритет выстрела
            if self.jumping:
                self.image = self.shooting_jump_image
            else:
                self.image = self.shooting_image
        elif self.jumping:
            if self.right:
                self.image = self.right_jump_image
            else:
                self.image = self.left_jump_image
        else:
            if self.right:
                self.image = self.right_image
            else:
                self.image = self.left_image


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

    def shoot(self, events):
        if not self.using_power_up:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self._fire_bullet()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._fire_bullet()

    def _fire_bullet(self):
        """Создаёт пулю и меняет картинку стрельбы"""
        self.shooting = True
        self.right = False
        self.left = False
        self.shooting_timer = pygame.time.get_ticks()  # Запоминаем время выстрела

        bullet = Bullet(self.rect.centerx, self.rect.top)  # Создаём пулю
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)


    def death(self):
        pass

    def update(self, keys, events):
        """Обновляет состояние игрока"""
        self.move(keys)
        self.apply_gravity()
        self.check_bounds()
        self.shoot(events)

        # Сбрасываем режим стрельбы через 200 мс
        if self.shooting and pygame.time.get_ticks() - self.shooting_timer > 200:
            self.shooting = False

        self.update_images()

    def check_platform_collision(self, platforms):
        for platform in platforms:
            if (
                self.rect.bottom >= platform.rect.top and
                self.rect.bottom <= platform.rect.top + 10 and
                self.rect.right > platform.rect.left and
                self.rect.left < platform.rect.right and
                self.velocity_y > 0
            ):
                if isinstance(platform, BrokenPlatform):
                    if not platform.broken:
                        platform.break_platform()
                    return

                self.rect.bottom = platform.rect.top
                self.velocity_y = -10
                self.jumping = True

                # Проверка на PowerUp
                if platform.power_up:
                    self.apply_power_ups(platform.power_up.power_up_type)
                    platform.power_up.kill()
                    platform.power_up = None
                break

    def apply_power_ups(self, power_up_type):
        if power_up_type == "jetpack":
            self.velocity_y = -65
        elif power_up_type == "spring":
            self.velocity_y = -30
        elif power_up_type == "trampoline":
            self.velocity_y = -45


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(join('assets', 'player', 'bullet.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        """Двигает пулю вверх"""
        self.rect.y -= 15

        all_sprites_group = self.groups()[0]
        if isinstance(all_sprites_group, AllSprites):
            offset_y = all_sprites_group.offset.y
        else:
            offset_y = 0

        # Учитываем оффсет при удалении пули
        if self.rect.bottom + offset_y < 0:
            self.kill()
