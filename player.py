import os

import pygame.image

from coin import Coin
from platforma import BrokenPlatform
from groups import AllSprites
from settings import *


class Player(pygame.sprite.Sprite):
    high_score = 0
    shield = 1
    def __init__(self, position, all_sprites, bullets):
        super().__init__()
        self.death_y = None
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.2

        self.direction = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(position[0], position[1], 50, 50)
        self.y = position[1]

        self.shield = False
        self.shield_timer = 0
        self.stars = False
        self.jumping = False
        self.left = False
        self.right = True
        self.shooting = False
        self.dead = False
        self.using_power_up = False
        self.shooting_timer = 0

        self.all_sprites = all_sprites
        self.bullets = bullets

        self.score = 0

        self.right_image = pygame.image.load(join('assets', 'player', 'right.png')).convert_alpha()
        self.left_image = pygame.image.load(join('assets', 'player', 'left.png')).convert_alpha()
        self.right_jump_image = pygame.image.load(join('assets', 'player', 'right_jump.png')).convert_alpha()
        self.left_jump_image = pygame.image.load(join('assets', 'player', 'left_jump.png')).convert_alpha()
        self.shooting_image = pygame.image.load(join('assets', 'player', 'shoot.png')).convert_alpha()
        self.shooting_jump_image = pygame.image.load(join('assets', 'player', 'shoot_jump.png')).convert_alpha()

        self.image = self.right_image


        self.jump_sound = pygame.mixer.Sound(join('assets', 'sounds', 'jump.wav'))
        self.break_platform_sound = pygame.mixer.Sound(join('assets', 'sounds', 'break.wav'))
        self.jetpack_sound = pygame.mixer.Sound(join('assets', 'sounds', 'jetpack.wav'))
        self.shoot_sound = pygame.mixer.Sound(join('assets', 'sounds', 'shoot_1.wav'))
        self.spring_sound = pygame.mixer.Sound(join('assets', 'sounds', 'spring.wav'))
        self.trampoline_sound = pygame.mixer.Sound(join('assets', 'sounds', 'trampoline.wav'))

        self.shield_right_img = pygame.image.load(join('assets', 'player', 'shield_right.png')).convert_alpha()
        self.shield_left_img = pygame.image.load(join('assets', 'player', 'shield_left.png')).convert_alpha()



    def update_images(self):
        if self.shooting:
            if self.jumping:
                self.image = self.shooting_jump_image
            else:
                self.image = self.shooting_image
        elif self.shield:
            if self.right:
                self.image = self.shield_right_img
            else:
                self.image = self.shield_left_img
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
        if not self.dead:
            self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            self.rect.x += self.direction.x * self.speed

            if self.direction.x > 0:
                self.right = True
                self.left = False
            elif self.direction.x < 0:
                self.right = False
                self.left = True

    def apply_gravity(self):
        if not self.dead:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y


    def reset_position(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - self.rect.height - 10
        self.velocity_y = 0

    def check_bounds(self):
        if self.rect.left < 0:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.right > WIDTH:
            self.rect.x = 0

    def shoot(self, events):
        if not self.dead:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.fire_bullet()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.fire_bullet()

    def fire_bullet(self):
        self.shooting = True
        self.right = False
        self.left = False
        self.shooting_timer = pygame.time.get_ticks()
        self.shoot_sound.play()

        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def update(self, keys, events, platforms, monsters, coins):
        self.move(keys)
        self.apply_gravity()
        self.check_bounds()
        self.shoot(events)
        self.check_collision_monster(monsters)
        self.check_platform_collision(platforms)
        self.check_collision_coin(coins)
        self.update_images()
        self.update_score()
        if self.shooting and pygame.time.get_ticks() - self.shooting_timer > 200:
            self.shooting = False
        if platforms:
            lowest_platform = max(platforms, key=lambda p: p.rect.top)
            if self.rect.top > lowest_platform.rect.top + 50:
                self.dead = True
        if self.shield and pygame.time.get_ticks() - self.shield_timer > 5000:
            self.deactivate_shield()
        if keys[pygame.K_z]:
            self.activate_shield()

    def check_platform_collision(self, platforms):
        if not self.dead:
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
                            self.break_platform_sound.play()
                        return

                    self.rect.bottom = platform.rect.top
                    self.velocity_y = -10
                    self.jumping = True
                    self.jump_sound.play()

                    self.using_power_up = False

                    if platform.power_up:
                        self.apply_power_ups(platform.power_up.power_up_type)
                        platform.power_up.kill()
                        platform.power_up = None
                    break

    def check_collision_monster(self, monsters):
        if not self.using_power_up:
            for monster in monsters:
                if monster.rect.colliderect(self.rect):
                    if self.shield:
                        self.deactivate_shield()
                        monster.kill()
                        monsters.remove(monster)
                    else:
                        self.dead = True

    def check_collision_coin(self, coins):
        if not self.using_power_up:
            for coin in coins:
                if coin.rect.colliderect(self.rect):
                    coin.kill()
                    coins.remove(coin)
                    Coin.coin_count += 1

    def apply_power_ups(self, power_up_type):
        self.using_power_up = True
        if power_up_type == "jetpack":
            self.velocity_y = -65
            self.jetpack_sound.play()
        elif power_up_type == "spring":
            self.velocity_y = -30
            self.spring_sound.play()
        elif power_up_type == "trampoline":
            self.velocity_y = -45
            self.trampoline_sound.play()

    def activate_shield(self):
        if Player.shield > 0:
            Player.shield -= 1
            self.shield = True
            self.shield_timer = pygame.time.get_ticks()

    def deactivate_shield(self):
        self.shield = False

    def update_score(self):
        self.score = max(self.score, abs(self.rect.top - HEIGHT))
        Player.high_score = max(Player.high_score, self.score)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(join('assets', 'player', 'bullet.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 15

        all_sprites_group = self.groups()[0]
        if isinstance(all_sprites_group, AllSprites):
            offset_y = all_sprites_group.offset.y
        else:
            offset_y = 0

        if self.rect.bottom + offset_y < 0:
            self.kill()
