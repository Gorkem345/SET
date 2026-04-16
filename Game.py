import pygame
import sys
from StartScreen import StartScreen
from GameScreen import GameScreen
from Rules import RulesScreen
from constants import WHITE, LIGHT, DARK, BG

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720))

        self.font = pygame.font.SysFont("Corbel", 40)
        self.sub_font = pygame.font.SysFont("Corbel", 25)
        self.title_font = pygame.font.SysFont("Corbel", 60)

        self.start_screen = StartScreen(self)
        self.game_screen = GameScreen(self)
        self.rules_screen = RulesScreen(self)

        self.current_screen = self.start_screen
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.current_screen.handle_event(event)

            self.current_screen.draw(self.screen)
            pygame.display.update()

        pygame.quit()
        sys.exit()


Game().run()