from settings import *
from player import Player
import sys

pygame.init()

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump Clone")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Создание игрока
        self.player = Player((WIDTH // 2, HEIGHT - 60))

        # Состояние игры
        self.running = True

    def run(self):
        while self.running:
            self.screen.fill(BLACK)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Управление игроком
            keys = pygame.key.get_pressed()
            self.player.update(keys)

            # Рисование игрока
            pygame.draw.rect(self.screen, BLUE, self.player.rect)

            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

# Запуск игры
if __name__ == "__main__":
    game = Main()
    game.run()
