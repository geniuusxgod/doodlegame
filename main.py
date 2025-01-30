
from settings import *
from player import Player
from platforma import Platform, MovingPlatformHorizontal, BrokenPlatform
from groups import AllSprites
import sys

pygame.init()


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump Clone")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load(join("assets", "background", "bg.png")).convert_alpha()

        self.all_sprites = AllSprites()
        self.bullets = pygame.sprite.Group()

        self.player = Player((WIDTH // 2, HEIGHT - 60), self.all_sprites, self.bullets)
        self.all_sprites.add(self.player)

        self.platforms = pygame.sprite.Group()
        self.create_initial_platforms()
        self.power_ups = pygame.sprite.Group()

        self.running = True

    def create_initial_platforms(self):
        for i in range(7):
            x = random.randint(0, WIDTH - 70)
            y = HEIGHT - i * 100
            platform_type = random.choices(
                [Platform, MovingPlatformHorizontal],
                weights=[0.8, 0.2],
                k=1
            )[0]
            platform = platform_type(x, y, 70, 10, False)
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
                weights=[0.8, 0.1, 0.1],
                k=1
            )[0]

            has_power_up = random.random() < 0.1
            platform = platform_type(x, y, 70, 10, has_power_up)

            if not self.check_platform_collision(platform, self.platforms):
                self.platforms.add(platform)
                self.all_sprites.add(platform)
                if platform.power_up:
                    self.power_ups.add(platform.power_up)
                    self.all_sprites.add(platform.power_up)

                if isinstance(platform, BrokenPlatform):
                    for _ in range(5):
                        additional_x = x + random.choice([-100, 100])
                        additional_x = max(0, min(WIDTH - 70, additional_x))
                        additional_y = y - random.randint(30, 50)

                        additional_platform = Platform(additional_x, additional_y, 70, 10)

                        if not self.check_platform_collision(additional_platform, self.platforms):
                            self.platforms.add(additional_platform)
                            self.all_sprites.add(additional_platform)
                            break


    def check_platform_collision(self, new_platform, platforms):
        for platform in platforms:
            if new_platform.rect.colliderect(platform.rect):
                return True
        return False

    def remove_offscreen_platforms(self):
        for platform in self.platforms:
            if platform.rect.top - 100 + self.all_sprites.offset.y > HEIGHT:
                platform.kill()
                self.all_sprites.remove(platform)
                self.platforms.remove(platform)
                if platform.power_up:
                    platform.power_up.kill()
                    self.all_sprites.remove(platform.power_up)
                    self.power_ups.remove(platform.power_up)


    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            self.player.update(keys, events)
            self.bullets.update()
            self.player.check_platform_collision(self.platforms)

            for platform in self.platforms:
                platform.update(0)

            if self.player.rect.top <= HEIGHT // 2:
                self.all_sprites.offset.y = -(self.player.rect.top - HEIGHT // 2)

            self.generate_new_platforms()
            self.remove_offscreen_platforms()

            self.all_sprites.draw(self.player.rect.center)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Main()
    game.run()