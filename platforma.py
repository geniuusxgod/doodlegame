from coin import Coin
from power_up import PowerUp
from settings import *

class Platform(pygame.sprite.Sprite):
    platform_sheet = pygame.image.load(join('assets', 'platforms+monsters', 'platform+monsters.png'))
    default_platform_image = platform_sheet.subsurface(pygame.Rect(1, 1, 57, 15))
    moving_hor_platform_image = platform_sheet.subsurface(pygame.Rect(2, 19, 58, 17))
    moving_vert_platform_image = platform_sheet.subsurface(pygame.Rect(2, 37, 58, 17))
    broken_platform_image1 = platform_sheet.subsurface(pygame.Rect(1, 73, 60, 15))
    broken_platform_image2 = platform_sheet.subsurface(pygame.Rect(0, 90, 62, 20))
    broken_platform_image3 = platform_sheet.subsurface(pygame.Rect(0, 116, 62, 27))
    broken_platform_image4 = platform_sheet.subsurface(pygame.Rect(0, 148, 62, 32))
    def __init__(self, x, y, width, height, has_power_up=False, has_coin=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = self.default_platform_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.power_up = None
        self.coins = None
        if has_power_up:
            self.create_power_up()
        if has_coin:
            self.create_coin()

    def update(self):
        pass

    def create_power_up(self):
        power_up_type = random.choice(["jetpack", "spring", "trampoline"])
        power_up_x = self.rect.centerx
        power_up_y = self.rect.top + 5
        self.power_up = PowerUp(power_up_x, power_up_y, power_up_type)

    def create_coin(self):
        x = self.rect.centerx
        y = self.rect.top - 2
        self.coins = Coin(x, y)

class MovingPlatformHorizontal(Platform):
    def __init__(self, x, y, width, height, has_power_up=False, has_coin=False):
        super().__init__(x, y, width, height)
        self.direction = 1
        self.image = self.moving_hor_platform_image
        self.speed = 2

        if has_coin:
            self.create_coin()

        if has_power_up:
            self.create_power_up()

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1

    def create_power_up(self):
        pass

    def create_coin(self):
        pass


class BrokenPlatform(Platform):
    def __init__(self, x, y, width, height, has_power_up=False, has_coin=False):
        super().__init__(x, y, width, height)
        self.image = self.broken_platform_image1
        self.broken = False
        self.speed_fall = 7
        self.animation_frames = [
            self.broken_platform_image1,
            self.broken_platform_image2,
            self.broken_platform_image3,
            self.broken_platform_image4,
        ]
        self.animation_index = 0
        self.animation_speed = 1
        self.animation_timer = 0

        if has_power_up:
            self.create_power_up()

        if has_coin:
            self.create_coin()

    def break_platform(self):
        self.broken = True

    def update(self):
        if not self.broken:
            super().update()
        else:
            self.animate_destruction()

    def animate_destruction(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.animation_index += 1
            if self.animation_index < len(self.animation_frames):
                self.image = self.animation_frames[self.animation_index]
            else:
                self.rect.y += self.speed_fall
                if self.rect.top >= HEIGHT:
                    self.kill()


    def create_power_up(self):
        pass