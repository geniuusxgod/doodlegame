from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Зелёный цвет платформ
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, velocity_y):
        """
        Смещает платформу вниз на заданную скорость (velocity_y).
        """
        self.rect.y += velocity_y


    @staticmethod
    def create_new_platform(last_platform_y, screen_width, platform_width, platform_height):
            """
            Создаёт новую платформу над экраном.
            """
            new_platform_y = last_platform_y - random.randint(80, 120)
            new_platform_x = random.randint(0, screen_width - platform_width)
            platform_type = random.choice([Platform, MovingPlatformHorizontal, MovingPlatformVertical])
            return platform_type(new_platform_x, new_platform_y, platform_width, platform_height)


class MovingPlatformHorizontal(Platform):
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        super().__init__(x, y, width, height)
        self.direction = 1  # Направление движения (1 = вправо, -1 = влево)
        self.image.fill(color=(255, 0, 0))
        self.speed = 2  # Скорость движения

    def update(self, velocity_y):
        super().update(velocity_y)  # Движение вниз с общей скоростью
        self.rect.x += self.direction * self.speed
        # Меняем направление, если платформа доходит до края экрана
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1



class MovingPlatformVertical(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.direction = 1  # Направление движения (1 = вниз, -1 = вверх)
        self.speed = 2
        self.image.fill(color=(0, 0, 255))

    def update(self, velocity_y):
        super().update(velocity_y)  # Движение вниз с общей скоростью
        self.rect.y += self.direction * self.speed
        # Меняем направление, если платформа доходит до крайних позиций
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT // 2:
            self.direction *= -1