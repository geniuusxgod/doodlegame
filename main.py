from settings import *
from player import Player
from platforma import Platform
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
        """
        Создаёт стартовые платформы.
        """
        for i in range(7):  # Количество платформ на экране
            x = random.randint(0, WIDTH - 70)
            y = HEIGHT - i * 80
            platform = Platform(x, y, 70, 10)
            self.platforms.add(platform)



    def generate_new_platforms(self):
        while len(self.platforms) < 7:
            last_platform_y = min(platform.rect.y for platform in self.platforms)
            platform = Platform.create_new_platform(
                last_platform_y,
                WIDTH,
                70,  # Ширина платформы
                10  # Высота платформы
            )
            self.platforms.add(platform)

    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player.update(keys)

            # Проверяем столкновения с платформами
            self.player.check_collision(self.platforms)

            # Перемещаем платформы вниз, если игрок поднимается
            if self.player.rect.top <= HEIGHT // 2:
                for platform in self.platforms:
                    platform.update(abs(self.player.velocity_y))
                    if platform.rect.top > HEIGHT:
                        self.platforms.remove(platform)
                self.player.rect.y += abs(self.player.velocity_y)

            # Генерируем новые платформы
            self.generate_new_platforms()

            # Рисуем платформы и игрока
            self.platforms.draw(self.screen)

            self.screen.blit(self.player.image, self.player.rect.topleft)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Main()
    game.run()
