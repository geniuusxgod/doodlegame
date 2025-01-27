from settings import *
from player import Player
from platforma import Platform, MovingPlatformHorizontal, BrokenPlatform
import sys

pygame.init()

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump Clone")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(join('assets', 'font', 'DoodleJump.ttf'), 36)

        self.background = pygame.image.load(join("assets", "background", "bg.png")).convert_alpha()

        self.player = Player((WIDTH // 2, HEIGHT - 60))

        self.platforms = pygame.sprite.Group()
        self.create_initial_platforms()

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
            platform = platform_type(x, y, 70, 10)
            self.platforms.add(platform)

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

            platform = platform_type(x, y, 70, 10)


            if not self.check_platform_collision(platform, self.platforms):
                self.platforms.add(platform)


                if isinstance(platform, BrokenPlatform):
                    for _ in range(5):
                        additional_x = x + random.choice([-100, 100])
                        additional_x = max(0, min(WIDTH - 70, additional_x))
                        additional_y = y - random.randint(50, 70)

                        additional_platform = Platform(additional_x, additional_y, 70, 10)

                        if not self.check_platform_collision(additional_platform, self.platforms):
                            self.platforms.add(additional_platform)
                            break


    def check_platform_collision(self, new_platform, platforms):
        for platform in platforms:
            if new_platform.rect.colliderect(platform.rect):
                return True
        return False

    def remove_offscreen_platforms(self):
        for platform in self.platforms:
            if platform.rect.top > HEIGHT:
                self.platforms.remove(platform)

    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player.update(keys)

            self.player.check_collision(self.platforms)

            for platform in self.platforms:
                platform.update(0)


            if self.player.rect.top <= HEIGHT // 2:
                offset = abs(self.player.velocity_y)
                for platform in self.platforms:
                    platform.rect.y += offset
                self.player.rect.y += offset

            self.generate_new_platforms()
            self.remove_offscreen_platforms()

            self.platforms.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect.topleft)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Main()
    game.run()