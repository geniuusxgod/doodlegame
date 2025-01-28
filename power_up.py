from settings import *


class PowerUp(pygame.sprite.Sprite):
    sprite_sheet = pygame.image.load(join('assets', 'platforms+monsters', 'platform+monsters.png'))
    jetpack_def = sprite_sheet.subsurface(pygame.Rect(196, 263, 27, 37))
    spring_def = sprite_sheet.subsurface(pygame.Rect(404, 99, 17, 12))
    trampoline_def = sprite_sheet.subsurface(pygame.Rect(188, 98, 36, 14))


    def __init__(self, x, y, power_up_type):
        super().__init__()
        self.power_up_type = power_up_type
        if self.power_up_type == 'jetpack':
            self.image = self.jetpack_def
        elif self.power_up_type == 'spring':
            self.image = self.spring_def
        elif self.power_up_type == 'trampoline':
            self.image = self.trampoline_def

        self.x = x
        self.y = y - 10
        self.rect = self.image.get_rect(center=(self.x, self.y))










