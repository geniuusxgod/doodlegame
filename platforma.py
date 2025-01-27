from settings import *

class Platform(pygame.sprite.Sprite):
    platfrom_sheet = pygame.image.load(join('assets', 'platforms+monsters', 'platform+monsters.png'))
    default_platform_image = platfrom_sheet.subsurface(pygame.Rect(1, 1, 57, 15))
    moving_hor_platform_image = platfrom_sheet.subsurface(pygame.Rect(2, 19, 58, 17))
    moving_vert_platform_image = platfrom_sheet.subsurface(pygame.Rect(2, 37, 58, 17))
    broken_platform_image1 = platfrom_sheet.subsurface(pygame.Rect(1, 73, 60, 15))
    broken_platform_image2 = platfrom_sheet.subsurface(pygame.Rect(0, 90, 62, 20))
    broken_platform_image3 = platfrom_sheet.subsurface(pygame.Rect(0, 116, 62, 27))
    broken_platform_image4 = platfrom_sheet.subsurface(pygame.Rect(0, 148, 62, 32))
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = self.default_platform_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, velocity_y):
        self.rect.y += velocity_y


    @staticmethod
    def create_new_platform(last_platform_y, screen_width, platform_width, platform_height):
            new_platform_y = last_platform_y - random.randint(80, 120)
            new_platform_x = random.randint(0, screen_width - platform_width)
            platform_type = random.choice([Platform, MovingPlatformHorizontal, BrokenPlatform])
            return platform_type(new_platform_x, new_platform_y, platform_width, platform_height)


class MovingPlatformHorizontal(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.direction = 1
        self.image = self.moving_hor_platform_image
        self.speed = 2

    def update(self, velocity_y=0):
        self.rect.x += self.direction * self.speed
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1


class BrokenPlatform(Platform):
    def __init__(self, x, y, width, height):
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

    def break_platform(self):
        self.broken = True

    def update(self, velocity_y=0):
        if not self.broken:
            super().update(velocity_y)
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