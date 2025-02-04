import sys

from coin import Coin
from player import Player
from settings import *

class Shop:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(join('assets', 'font', 'DoodleJump.ttf'), 30)
        self.bg = pygame.image.load(join('assets', 'background', 'bg.png')).convert_alpha()
        self.shield_img = pygame.image.load(join('assets', 'shield', 'shield.png')).convert_alpha()
        self.shield_img = pygame.transform.scale(self.shield_img, (50, 50))
        self.items = {'Shield': 10}
        self.selected_item = "Shield"
        self.back_to_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        self.font_exit = pygame.font.Font(join('assets', 'font', 'DoodleJump.ttf'), 40)
        self.message = ""

    def draw(self):
        self.screen.blit(self.bg, (0,0))
        coins_text = self.font.render(f'Coins: {Coin.coin_count}', True, (255,0,0))
        self.screen.blit(coins_text, (290, 10))
        self.screen.blit(self.shield_img, (WIDTH//2-25, 100))
        item_text = self.font.render(f"Buy Shield - {self.items['Shield']} Coins", True, (255, 0, 0))
        self.item_text_rect = item_text.get_rect(topleft=(100, 160))
        self.screen.blit(item_text, self.item_text_rect.topleft)

        pygame.draw.rect(self.screen, (0, 0, 0), self.back_to_menu_button)

        back_text = self.font_exit.render("Back to Menu", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=self.back_to_menu_button.center)
        self.screen.blit(back_text, back_text_rect.topleft)

        if self.message:
            message_text = self.font.render(self.message, True, (0, 255, 0) if "buy" in self.message else (255, 0, 0))
            self.screen.blit(message_text, (40, 220))

    def buy_item(self):
        if Coin.coin_count >= self.items[self.selected_item]:
            Coin.coin_count -= self.items[self.selected_item]
            self.message = "You buy a shield"
            Player.shield += 1
        else:
            self.message = "You don't have enough coins"

    def run(self):
        while True:
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_to_menu_button.collidepoint(event.pos):
                        return "menu"
                    if self.item_text_rect.collidepoint(event.pos):
                        self.buy_item()

        return "menu"