from settings import *


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(join('assets', 'font', 'DoodleJump.ttf'), 50)
        self.font_exit = pygame.font.Font(join('assets', 'font', 'DoodleJump.ttf'), 70)
        self.bg = pygame.image.load(join('assets', 'background', 'bg.png')).convert_alpha()

        self.play_buttons = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 220, 75)
        self.play_button = pygame.image.load(join('assets', 'buttons', 'play.png')).convert_alpha()
        self.play_button_hover = pygame.image.load(join('assets', 'buttons', 'play_hover.png')).convert_alpha()
        self.shop_buttons = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 220, 75)
        self.exit_buttons = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 220, 75)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        title_text = self.font.render("Doodle Jump Clone", True, (0, 0, 0))
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        mouse_pos = pygame.mouse.get_pos()

        play_button_img = self.play_button_hover if self.play_buttons.collidepoint(mouse_pos) else self.play_button
        self.screen.blit(play_button_img, self.play_buttons.topleft)

        shop_text = self.font_exit.render("shop", True, (0, 0, 0))
        exit_text = self.font_exit.render("exit", True, (0, 0, 0))

        shop_text_rect = shop_text.get_rect(center=self.shop_buttons.center)
        exit_text_rect = exit_text.get_rect(center=self.exit_buttons.center)

        self.screen.blit(shop_text, shop_text_rect.topleft)
        self.screen.blit(exit_text, exit_text_rect.topleft)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_buttons.collidepoint(event.pos):
                    return "play"
                if self.shop_buttons.collidepoint(event.pos):
                    return "shop"
                if self.exit_buttons.collidepoint(event.pos):
                    return "exit"
        return None

    def run(self):
        while True:
            choice = self.handle_events()
            if choice:
                return choice
            self.draw()
