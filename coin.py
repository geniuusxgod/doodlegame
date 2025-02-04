from settings import *

class Coin(pygame.sprite.Sprite):
    coin_count = 10
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y - 10
        self.frames_index = 0

        self.sprite_sheet = pygame.image.load(join('assets', 'coins', 'coin.png'))
        self.coin1 = self.sprite_sheet.subsurface(pygame.Rect(1,1,18,18))
        self.coin2 = self.sprite_sheet.subsurface(pygame.Rect(21,1,18,18))
        self.coin3 = self.sprite_sheet.subsurface(pygame.Rect(41,1,18,18))
        self.coin4 = self.sprite_sheet.subsurface(pygame.Rect(64,1,13,18))
        self.coin5 = self.sprite_sheet.subsurface(pygame.Rect(84,1,10,18))
        self.coin6 = self.sprite_sheet.subsurface(pygame.Rect(104,1,13,18))
        self.coin7 = self.sprite_sheet.subsurface(pygame.Rect(121,1,18,18))
        self.coin8 = self.sprite_sheet.subsurface(pygame.Rect(141,1,18,18))
        self.coin9 = self.sprite_sheet.subsurface(pygame.Rect(161,1,18,18))
        self.frames = [self.coin1, self.coin2, self.coin3, self.coin4, self.coin5, self.coin6, self.coin7, self.coin8,
                       self.coin9]
        self.animation_speed = 5
        self.counter = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.frames_index = (self.frames_index + 1) % len(self.frames)
            self.image = self.frames[self.frames_index]
