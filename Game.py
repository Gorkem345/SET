import pygame
import sys
from screens.StartScreen import StartScreen
from screens.Multiplayer import Multiplayer
from screens.Rules import RulesScreen
from screens.WinnerScreen import WinnerScreen
from screens.TableDisplay import Display_card
from screens.settings_screen import SettingsScreen
from utils.set_table import Table
from screens.Singleplayer import SingleplayerScreen
from screens.ConfirmScreen import ConfirmScreen
from screens.PreStartScreen import PreStartScreen


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE | pygame.SCALED)
        pygame.mixer.init()

        self.turn_duration_ms = 300000

        #create font type and size
        self.font = pygame.font.SysFont("Corbel", 40)
        self.sub_font = pygame.font.SysFont("Corbel", 25)
        self.title_font = pygame.font.SysFont("Corbel", 60)
        self.small_font = pygame.font.SysFont("Corbel", 18)

        self.display_card = Display_card()
        self.table = Table()
        self.table.handle_start_game()

        #create different screens/pages
        self.start_screen = StartScreen(self)
        self.singleplayer_screen = SingleplayerScreen(self)
        self.game_screen = Multiplayer(self)
        self.rules_screen = RulesScreen(self)
        self.winner_screen = WinnerScreen(self)
        self.confirm_screen = ConfirmScreen(self)
        self.pre_start_screen = PreStartScreen(self)
        self.settings_screen = SettingsScreen(self)

        self.current_screen = self.start_screen
        self.running = True

        #add winner data
        self.winner = ""
        self.p1_score = 0
        self.p2_score = 0
        self.comp_score = 0
        self.point_gain = 1
        self.point_loss = 1

    def run(self):
        while self.running:
            # 1. Handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_screen.handle_event(event)
            # 2. Update Game Logic
            self.table.update()
            # 3. Draw the Screen
            self.current_screen.draw(self.screen)
            pygame.display.update()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run() # Game loop
