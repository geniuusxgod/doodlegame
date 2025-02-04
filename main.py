from coin import Coin
from power_up import PowerUp
from settings import *
from player import Player
from monster import Monster
from platforma import Platform, MovingPlatformHorizontal, BrokenPlatform
from groups import AllSprites
from playagain_menu import PlayAgainMenu
from main_menu import MainMenu
import sys

from shop import Shop

pygame.init()


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump Clone")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load(join("assets", "background", "bg.png")).convert_alpha()
        self.font = pygame.font.Font(join('assets', 'font', 'DoodleJump.ttf'), 30)

        self.all_sprites = AllSprites()
        self.bullets = pygame.sprite.Group()
        self.platform_count = 0
        self.monsters = pygame.sprite.Group()

        self.player = Player((WIDTH // 2, HEIGHT - 60), self.all_sprites, self.bullets)
        self.all_sprites.add(self.player)

        self.platforms = pygame.sprite.Group()
        self.create_initial_platforms()
        self.power_ups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.running = True


    def create_initial_platforms(self):
        first_platform = Platform(WIDTH // 2, HEIGHT, 70, 10, False)
        self.platforms.add(first_platform)
        self.all_sprites.add(first_platform)
        for i in range(6):
            x = random.randint(0, WIDTH - 70)
            y = HEIGHT - (i+1) * 100
            platform_type = random.choices(
                [Platform, MovingPlatformHorizontal],
                weights=[0.8, 0.2],
                k=1
            )[0]
            platform = platform_type(x, y, 70, 10, False)
            self.platform_count += 1
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def generate_new_platforms(self):
        if not self.platforms:
            y = HEIGHT
        else:
            y = min(platform.rect.y for platform in self.platforms) - random.randint(80, 150)

        while len(self.platforms) < 7:
            x = random.randint(0, WIDTH - 70)
            platform_type = random.choices(
                [Platform, MovingPlatformHorizontal, BrokenPlatform],
                weights=[0.6, 0.2, 0.2],
                k=1
            )[0]

            has_power_up = random.random() < 0.1
            has_coin = random.random() < 0.3
            platform = platform_type(x, y, 70, 10, has_power_up, has_coin)
            self.platform_count += 1

            if self.platform_count % 50 == 0:
                monster = Monster(platform.rect.top - 50)
                self.monsters.add(monster)
                self.all_sprites.add(monster)

            if not self.check_platform_collision(platform, self.platforms):
                self.platforms.add(platform)
                self.all_sprites.add(platform)
                if platform.power_up:
                    self.power_ups.add(platform.power_up)
                    self.all_sprites.add(platform.power_up)
                if platform.coins:
                    self.coins.add(platform.coins)
                    self.all_sprites.add(platform.coins)

                if isinstance(platform, BrokenPlatform):
                    for _ in range(5):
                        additional_x = x + random.choice([-100, 100])
                        additional_x = max(0, min(WIDTH - 70, additional_x))
                        additional_y = y - random.randint(30, 50)

                        additional_platform = Platform(additional_x, additional_y, 70, 10)
                        self.platform_count += 1

                        if not self.check_platform_collision(additional_platform, self.platforms):
                            self.platforms.add(additional_platform)
                            self.all_sprites.add(additional_platform)
                            break

    def check_platform_collision(self, new_platform, platforms):
        for platform in platforms:
            if new_platform.rect.colliderect(platform.rect):
                return True
        return False

    def remove_offscreen_object(self):
        for sprite in self.all_sprites:
            if sprite.rect.top - 100 + self.all_sprites.offset.y > HEIGHT:
                sprite.kill()
                self.all_sprites.remove(sprite)
                if isinstance(sprite, Platform):
                    self.platforms.remove(sprite)
                elif isinstance(sprite, PowerUp):
                    self.power_ups.remove(sprite)
                elif isinstance(sprite, Coin):
                    self.coins.remove(sprite)
                elif isinstance(sprite, Monster):
                    self.monsters.remove(sprite)

    def show_play_again_menu(self):
        play_again_menu = PlayAgainMenu(self.screen)
        choice = None

        while choice is None:
            play_again_menu.draw(self.player.score, Player.high_score)
            choice = play_again_menu.handle_events()

        if choice == "restart":
            self.__init__()
            self.run()
        elif choice == "menu":
            main_menu = MainMenu(self.screen)
            choice = main_menu.run()

            if choice == "play":
                self.__init__()
                self.run()
            elif choice == "shop":
                shop = Shop(self.screen)
                shop.run()
            else:
                pygame.quit()
                sys.exit()

    def draw_score(self, screen, score, coins):
        score_text = self.font.render(f'Score: {score}', True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        coins_text = self.font.render(f'Coins: {coins}', True, (255, 0, 0))
        screen.blit(coins_text, (290, 10))

    def run_shop(self):
        shop_menu = Shop(self.screen)
        result = shop_menu.run()
        if result == "menu":
            return

    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            self.player.update(keys, events, self.platforms, self.monsters, self.coins)
            self.bullets.update()
            self.monsters.update(self.bullets)
            self.coins.update()

            for platform in self.platforms:
                platform.update()

            if self.player.rect.top <= HEIGHT // 2:
                self.all_sprites.offset.y = -(self.player.rect.top - HEIGHT // 2)

            if self.player.dead:
                self.show_play_again_menu()

            self.generate_new_platforms()
            self.remove_offscreen_object()

            self.all_sprites.draw(self.player.rect.center)
            self.draw_score(self.screen, self.player.score, Coin.coin_count)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    while True:
        menu = MainMenu(screen)
        choice = menu.run()

        if choice == "play":
            game = Main()
            game.run()
        elif choice == "shop":
            shop = Shop(screen)
            shop.run()
        else:
            pygame.quit()
            sys.exit()