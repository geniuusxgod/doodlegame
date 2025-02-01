from settings import *


class Monster(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load(join('assets', 'platforms+monsters', 'platform+monsters.png'))
        self.image = self.sprite_sheet.subsurface(pygame.Rect(308,3,81,42))
        self.rect = self.image.get_rect(center=(WIDTH // 2, y))
        self.die_sound = pygame.mixer.Sound(join('assets', 'sounds', 'die_1.wav'))
        self.start_x = self.rect.x
        self.direction = 1
        self.speed = 2
        self.range = 70
        self.monster_sound = pygame.mixer.Sound(join('assets', 'sounds', 'monster.wav'))
        self.monster_sound.play()

    def update(self, bullets):
        self.rect.x += self.speed * self.direction

        if abs(self.rect.x - self.start_x) >= self.range:
            self.direction *= -1

        self.check_collision_bullet(bullets)

    def check_collision_bullet(self, bullets):
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                self.kill()
                bullet.kill()
                self.die_sound.play()