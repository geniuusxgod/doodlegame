from settings import *
import pygame


class PlayAgainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(join("assets", "font", "DoodleJump.ttf"), 40)
        self.bg = pygame.image.load(join("assets", "background", "bg.png")).convert_alpha()

        self.sprite_sheet = pygame.image.load(join("assets", "buttons", "start-end-tiles.png"))

        self.play_again_buttons = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 220, 75)
        self.menu_buttons = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 220, 75)

        self.play_again_button = self.sprite_sheet.subsurface(pygame.Rect(228,97,229,84))
        self.play_again_button_hover = pygame.image.load(join("assets", "buttons", "play_again_hover.png")).convert_alpha()

        self.menu_button_image = self.sprite_sheet.subsurface(pygame.Rect(2,97,225,84))
        self.menu_button_hover = pygame.image.load(join("assets", "buttons", "menu_hover.png")).convert_alpha()

    def draw(self, score, high_score):
        self.screen.blit(self.bg, (0, 0))  # Фон
        game_over_text = self.font.render("game over!", True, (255, 0, 0))
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 180))

        score_text = self.font.render(f'score: {score}', True, (255, 0, 0))
        high_score = self.font.render(f'high score: {high_score}', True, (255, 0, 0))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 140))
        self.screen.blit(high_score, (WIDTH // 2 - high_score.get_width() // 2, HEIGHT // 2 - 100))

        mouse_pos = pygame.mouse.get_pos()

        play_again_button_img = self.play_again_button_hover if self.play_again_buttons.collidepoint(mouse_pos) else self.play_again_button
        self.screen.blit(play_again_button_img, self.play_again_buttons.topleft)

        # Menu
        menu_button_img = self.menu_button_hover if self.menu_buttons.collidepoint(mouse_pos) else self.menu_button_image
        self.screen.blit(menu_button_img, self.menu_buttons.topleft)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_buttons.collidepoint(event.pos):
                    return "restart"
                if self.menu_buttons.collidepoint(event.pos):
                    return "menu"
        return None
